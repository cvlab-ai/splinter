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
from src.utils.exceptions import ExamNotDetected


class Controller:
    @staticmethod
    def check_pdf(request: CheckPdfDTO):
        _check_pdf(
            request.exam_id, request.file_name, PDFType.answer_sheets, request.force
        )

    @staticmethod
    def check_exam(request: CheckExamDTO):
        logging.info(f"Checking exam: {request.exam_id}")
        files = remote_storage.get_pdfs_names(request.exam_id, PDFType.answer_sheets)
        if files is None:
            return
        for file_name in files:
            logging.info(f"Checking answer pdf: {file_name}")
            _check_pdf(request.exam_id, file_name, PDFType.answer_sheets, request.force)

    @staticmethod
    def generate_exam_keys(request: GenerateExamKeysDTO):
        logging.info(f"Generating answer keys for exam: {request.exam_id}")
        files = remote_storage.get_pdfs_names(request.exam_id, PDFType.answer_keys)
        if files is None:
            return
        for file_name in files:
            logging.info(f"Checking answer key pdf: {file_name}")
            _check_pdf(request.exam_id, file_name, PDFType.answer_keys, request.force)


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
                results = _check_image(image)
            except ExamNotDetected as e:
                logging.warning(f"Error during processing page {i + 1} in file {file_name}: {e}")
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
                sufix = versioning.get_group_suffix(results)
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


def _check_image(image: Image) -> ResultsDTO:
    fields_images = Preprocessing(np.asarray(image)).process()
    ocr_model = OCRModel(Config.paths.ocr_model_path)
    box_model = BoxModel(Config.paths.box_model_path)

    results = {
        Fields.exam_title.name: ocr_model.inference(fields_images[Fields.exam_title][0]),
        Fields.student_name.name: ocr_model.inference(fields_images[Fields.student_name][0]),
        Fields.date.name: ocr_model.inference(fields_images[Fields.date][0]),
        f"{Fields.student_id.name}_text": ocr_model.inference(fields_images[Fields.student_id][0][1], only_digits=True),
        f"{Fields.student_id.name}_boxes": box_model.inference(fields_images[Fields.student_id][0][0], argmax=True),
        Fields.exam_key.name: box_model.inference(fields_images[Fields.exam_key]),
        Fields.answers.name: box_model.inference(fields_images[Fields.answers])
    }
    output = ResultsDTO.parse_obj(results)
    logging.info("Inference results:\n" + str(output))
    return output
