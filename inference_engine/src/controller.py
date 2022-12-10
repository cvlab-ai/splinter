import logging
import tempfile
from pathlib import Path

import numpy as np
from PIL.Image import Image

from src.config import Config
from src.dto import CheckExamDTO, CheckPdfDTO, GenerateExamKeysDTO
from src.dto.results_dto import ResultsDTO
from src.exam_storage import local_storage, metadata, remote_storage, versioning
from src.exam_storage.pdf_type import PDFType
from src.model import BoxModel, OCRModel
from src.preprocessing import Fields, Preprocessing
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
                results = _check_image(image, pdf_type == PDFType.answer_sheets)
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
            local_storage.save_answers_to_dir(
                output_dir,
                results,
                version=version,
                image=image,
                sufix=sufix,
            )
        remote_storage.push_dir(
            tmp_dir, remote_storage.get_output_path(exam_id, pdf_type), recursive=True
        )
        metadata.mark_pdf_done(exam_id, file_name, pdf_type)


def _check_image(image: Image, check_index: bool) -> ResultsDTO:
    fields_images = Preprocessing(np.asarray(image)).process()
    ocr_model = OCRModel(Config.paths.ocr_model_path)
    box_model = BoxModel(Config.paths.box_model_path)
    index, predictions = box_model.inference(fields_images[Fields.student_id][0][0], argmax=True)
    if check_index and predictions.min() < Config.inference.answer_threshold:
        raise IndexNotDetected("Didn't detect 6 index numbers")

    results = {
        Fields.exam_title.name: ocr_model.inference(fields_images[Fields.exam_title][0]),
        Fields.student_name.name: ocr_model.inference(fields_images[Fields.student_name][0]),
        Fields.date.name: ocr_model.inference(fields_images[Fields.date][0]),
        f"{Fields.student_id.name}_text": ocr_model.inference(fields_images[Fields.student_id][0][1], only_digits=True),
        f"{Fields.student_id.name}_boxes": index,
        Fields.exam_key.name: box_model.inference(fields_images[Fields.exam_key]),
        Fields.answers.name: box_model.inference(fields_images[Fields.answers])
    }
    output = ResultsDTO.parse_obj(results)
    logging.info("Inference results:\n" + str(output))
    return output
