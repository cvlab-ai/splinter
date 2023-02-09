import typing as tp
import logging
import tempfile
from pathlib import Path

import numpy as np
import cv2
from PIL.Image import Image

from src.config import Config
from src.dto import CheckExamDTO, CheckPdfDTO, GenerateExamKeysDTO
from src.dto.results_dto import ResultsDTO
from src.exam_storage import local_storage, metadata, remote_storage, versioning
from src.exam_storage.pdf_type import PDFType
from src.model import BoxModel, OCRModel
from src.preprocessing import FieldName, Preprocessing, Field
from src.utils.exceptions import IndexNotDetected, ExamInvalid
from src import score


# Wrapper function for controller methods that affects exam scores
def update_scores(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        for arg in args:
            if hasattr(arg, "exam_id"):
                _update_exam_scores(arg.exam_id)
                break
    return wrapper


class Controller:
    @staticmethod
    @update_scores
    def check_pdf(request: CheckPdfDTO):
        _generate_exam_keys(request.exam_id)
        logging.info(f"Checking answer pdf: {request.file_name}")
        _check_pdf(
            request.exam_id, request.file_name, PDFType.answer_sheets, request.force
        )

    @staticmethod
    @update_scores
    def check_exam(request: CheckExamDTO):
        _generate_exam_keys(request.exam_id)
        logging.info(f"Checking exam: {request.exam_id}")
        files = remote_storage.get_pdfs_names(request.exam_id, PDFType.answer_sheets)
        if files is None:
            return
        for file_name in files:
            logging.info(f"Checking answer pdf: {file_name}")
            _check_pdf(request.exam_id, file_name, PDFType.answer_sheets, request.force)

    @staticmethod
    @update_scores
    def generate_exam_keys(request: GenerateExamKeysDTO):
        _generate_exam_keys(request.exam_id, force=request.force)


def _generate_exam_keys(exam_id, force=False):
    logging.info(f"Generating answer keys for exam: {exam_id}")
    files = remote_storage.get_pdfs_names(exam_id, PDFType.answer_keys)
    if files is None:
        return
    for file_name in files:
        logging.info(f"Checking answer key pdf: {file_name}")
        _check_pdf(exam_id, file_name, PDFType.answer_keys, force)


def _update_exam_scores(exam_id: int):
    logging.info(f"Updating scores for exam: {exam_id}")
    students_result = remote_storage.get_students_results(exam_id)
    answers_keys = remote_storage.get_answer_keys(exam_id)
    if not answers_keys:
        logging.info("No answer key to use in score calculation")
        return
    if not students_result:
        logging.info("No student answers to calculate score")
        return
    with tempfile.TemporaryDirectory() as tmp, Path(tmp) as tmp_dir:
        with open(tmp_dir/"scores.csv", "w") as result_file:
            score_csv = score.ScoreCSV(result_file)
            score_csv.write_scores(students_result, answers_keys)
        remote_storage.push_dir(tmp_dir,f"{exam_id}")


def _check_pdf(exam_id, file_name, pdf_type: PDFType, force=False):
    if not force and metadata.check_pdf_processed(exam_id, file_name, pdf_type):
        logging.info(f"PDF {file_name} already checked, skipping.")
        return
    with tempfile.TemporaryDirectory() as tmp, Path(tmp) as tmp_dir:
        images = remote_storage.unpack_pdf(
            f"{remote_storage.get_input_path(exam_id, pdf_type)}/{file_name}"
        )
        if images is None:
            logging.info(f"PDF {file_name} doesn't contains any images.")
            return
        for i, image in enumerate(images):
            try:
                results, debug_img = _check_image(image, pdf_type == PDFType.answer_sheets)
            except ExamInvalid as e:
                logging.warning(f"Error during processing page {i + 1} in file {file_name}: {e}")
                output_dir = tmp_dir / e.FILENAME
                output_dir.mkdir(exist_ok=True)
                image.save(f"{output_dir}/unknown_{i}.jpg", "JPEG")
                continue
            output_dir = tmp_dir
            sufix = ""
            if pdf_type == PDFType.answer_sheets:
                output_dir = output_dir / results.student_id_boxes
                version = versioning.get_next_version(
                    output_dir,
                    remote_storage.get_student_dir(exam_id, index=results.student_id_boxes),
                )
            elif pdf_type == PDFType.answer_keys:
                sufix = "_" + versioning.examkey2group(results.exam_key)
                version = versioning.get_next_version(
                    output_dir, remote_storage.get_answer_key_dir(exam_id), sufix=sufix
                )
            local_storage.save_answers_to_dir(output_dir, results, version=version, image=image, debug_image=debug_img,
                                              sufix=sufix)
        remote_storage.push_dir(
            tmp_dir, remote_storage.get_output_path(exam_id, pdf_type), recursive=True
        )
        metadata.mark_pdf_done(exam_id, file_name, pdf_type)


def _check_image(image: Image, check_index: bool) -> tp.Tuple[ResultsDTO, np.ndarray]:
    fields_images, debug_image = Preprocessing(np.asarray(image)).process()
    ocr_model = OCRModel(Config.paths.ocr_model_path)
    box_model = BoxModel(Config.paths.box_model_path)
    index, predictions = box_model.inference(fields_images[FieldName.student_id][0][0].img, argmax=True)
    index = ''.join([str(i) if p > Config.inference.answer_threshold else 'X' for i, p in zip(index, predictions)])
    answers_img = np.array([f.img for f in fields_images[FieldName.answers]])
    answers_img = answers_img.reshape(-1, *answers_img.shape[2:])

    results = {
        FieldName.exam_title.name: ocr_model.inference(fields_images[FieldName.exam_title][0].img),
        FieldName.student_name.name: ocr_model.inference(fields_images[FieldName.student_name][0].img),
        FieldName.date.name: ocr_model.inference(fields_images[FieldName.date][0].img),
        f"{FieldName.student_id.name}_text": ocr_model.inference(fields_images[FieldName.student_id][0][1].img, only_digits=True),
        f"{FieldName.student_id.name}_boxes": index,
        FieldName.exam_key.name: box_model.inference(fields_images[FieldName.exam_key][0].img),
        FieldName.answers.name: box_model.inference(answers_img)
    }
    output = ResultsDTO.parse_obj(results)
    logging.info("Inference results:\n" + str(output))

    if not Config.inference.debug_image:
        return output, None

    try:
        debug_image = highlight_marks(debug_image, fields_images, output)
    except Exception:
        logging.exception("Cannot create inference debug image")
        return output, None

    return output, debug_image


def highlight_marks(debug_image: np.ndarray, fields: tp.Dict[FieldName, tp.List[Field]], results: ResultsDTO):
    debug_image = cv2.cvtColor(debug_image, cv2.COLOR_GRAY2RGB)
    white = (255, 255, 255)

    def highlight_mark(x: int, y: int, w: int, h: int, rgb: tp.Tuple[int, int, int] = white):
        reverse_rgb = (255 - np.array(rgb)).astype(np.uint8)
        crop = debug_image[y: y + h, x: x + w].astype(np.int32) - reverse_rgb
        crop[crop < 0] = 0
        debug_image[y: y + h, x: x + w] = crop

    def highlight_row(row_results, rect: tp.Tuple[int, int, int, int], rgb: tp.Tuple[int, int, int] = white):
        width = rect[2] // len(row_results)
        for i, is_marked in enumerate(row_results):
            if is_marked:
                x = rect[0] + width * i
                highlight_mark(x, rect[1], width, rect[3], rgb=rgb)

    def highlight_answer_columns(rgb: tp.Tuple[int, int, int] = white):
        number_of_rows = len(results.answers) // len(fields[FieldName.answers])
        for i, row in enumerate(results.answers.values()):
            column_index = i // number_of_rows
            field = fields[FieldName.answers][column_index]
            # Row height is a height of column divided by number of rows
            height = field.rect[3] // field.img.shape[0]
            y = field.rect[1] + i % number_of_rows * height
            highlight_row(row, (field.rect[0], y, field.rect[2], height), rgb=rgb)

    def highlight_index_columns(rect: tp.Tuple[int, int, int, int], index: str, rgb: tp.Tuple[int, int, int] = white):
        w = rect[2] // 6
        h = rect[3] // 10
        for i, number in enumerate(index):
            x = rect[0] + w * i
            y = rect[1] + h * int(number)
            highlight_mark(x, y, w, h, rgb)

    # Text fields
    text_color = (235, 255, 235)
    highlight_mark(*fields[FieldName.exam_title][0].rect, rgb=text_color)
    highlight_mark(*fields[FieldName.student_name][0].rect, rgb=text_color)
    highlight_mark(*fields[FieldName.date][0].rect, rgb=text_color)
    highlight_mark(*fields[FieldName.student_id][0][1].rect, rgb=text_color)

    # Box fields
    box_color = (255, 235, 235)
    highlight_mark(*fields[FieldName.exam_key][0].rect, rgb=box_color)
    highlight_mark(*fields[FieldName.student_id][0][0].rect, rgb=box_color)
    [highlight_mark(*f.rect, rgb=box_color) for f in fields[FieldName.answers]]

    # Marks
    mark_color = (120, 255, 120)
    highlight_row(results.exam_key, fields[FieldName.exam_key][0].rect, rgb=mark_color)
    highlight_answer_columns(rgb=mark_color)
    highlight_index_columns(fields[FieldName.student_id][0][0].rect, results.student_id_boxes, rgb=mark_color)
    return debug_image
