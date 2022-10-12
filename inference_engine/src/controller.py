import logging

import numpy as np
from json import dumps

from src.config import Config
from .storage import Storage
from .preprocessing import Preprocessing
from .model import AnswerModel, IndexModel
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
        answer_input, index_input = Preprocessing(image).process()
        index_result = IndexModel(Config.paths.index_model_path).inference(index_input)
        logging.info(f"Detected index: {index_result}")
        answer_result = AnswerModel(Config.paths.answer_model_path).inference(answer_input)
        logging.info(f"Detected answers: {Controller._get_readable_answers(answer_result)}")
        json_result = Controller._create_output_json(answer_result, index_result)
        Storage.set_exam_answer_json(output_path, file_name, json_result)

    @staticmethod
    def _create_output_json(answers: np.ndarray, index: str):
        return {
            "index": index,
            "answers": {i + 1: [int(answer) for answer in row] for i, row in enumerate(answers)}
        }

    @staticmethod
    def _get_readable_answers(answers: np.ndarray) -> str:
        return dumps({i + 1: ', '.join(
            [chr(ord('A') + idx) for idx, val in enumerate(answer) if val]
        ) for i, answer in enumerate(answers) if np.any((answer == 1))}, indent=4)
