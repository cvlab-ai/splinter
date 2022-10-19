import typing as tp
import logging

import numpy as np
from json import dumps

from src.config import Config
from .storage import Storage
from .preprocessing import Preprocessing, Fields
from .model import AnswerModel, OCRModel
from .dto import CheckExamsDTO, CheckExamDTO, GenerateExamKeyDTO


class Controller:
    @staticmethod
    def check_exam(request: CheckExamDTO):
        input_dir = Controller._add_io_path(request.exam_path, Config.exam_storage.default_input_dirname)
        output_dir = Controller._add_io_path(request.exam_path, Config.exam_storage.default_output_dirname)
        Controller._mark_detection(input_dir, request.exam_name, output_dir)

    @staticmethod
    def check_exams(request: CheckExamsDTO):
        input_dir = Controller._add_io_path(request.exam_path, Config.exam_storage.default_input_dirname)
        output_dir = Controller._add_io_path(request.exam_path, Config.exam_storage.default_output_dirname)
        for exam_name in Storage.get_exams_names(input_dir):
            Controller._mark_detection(input_dir, exam_name, output_dir)

    @staticmethod
    def generate_exam_key(request: GenerateExamKeyDTO):
        Controller._mark_detection(request.exam_path, f'{Config.exam_storage.full_answer_image_filename}',
                                   request.exam_path)

    @staticmethod
    def _add_io_path(exam_path: str, io_path: str):
        return f"{exam_path}/{io_path}/"

    @staticmethod
    def _mark_detection(file_path: str, file_name: str, output_path: str):
        image = Storage.get_exam_image(file_path, file_name)
        fields_images = Preprocessing(image).process()
        ocr_model = OCRModel(Config.paths.index_model_path)

        ocr_results = {f: ocr_model.inference(fields_images[f][0], True if f == Fields.student_id else False)
                       for f in Fields.ocr_fields()}
        for field, result in ocr_results.items():
            logging.info(f"Detected {field.name}: {result}")

        box_model = AnswerModel(Config.paths.answer_model_path)

        exam_key_result = box_model.inference(fields_images[Fields.exam_key])
        logging.info(f"Detected exam key: {Controller._get_readable_answers(exam_key_result)}")

        answer_result = box_model.inference(fields_images[Fields.answer_column])
        logging.info(f"Detected answers: {Controller._get_readable_answers(answer_result)}")

        json_result = Controller._create_output_json(answer_result, ocr_results)
        Storage.set_exam_answer_json(output_path, file_name, json_result)

    @staticmethod
    def _create_output_json(answers: np.ndarray, ocr_results: tp.Dict[Fields, str]):
        _json = {f.name: result for f, result in ocr_results.items()}
        _json["answers"] = {i + 1: [int(answer) for answer in row] for i, row in enumerate(answers)}
        return _json

    @staticmethod
    def _get_readable_answers(answers: np.ndarray) -> str:
        return dumps({i + 1: ', '.join(
            [chr(ord('A') + idx) for idx, val in enumerate(answer) if val]
        ) for i, answer in enumerate(answers) if np.any((answer == 1))}, indent=4)
