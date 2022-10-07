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
        return Controller._mark_detection(request.exam_path, request.exam_name)

    @staticmethod
    def check_exams(request: CheckExamsDTO):
        for exam_name in Storage.get_exams_names(request.exam_path):
            Controller._mark_detection(request.exam_path, exam_name)

    @staticmethod
    def generate_exam_key(request: GenerateExamKeyDTO):
        return Controller._mark_detection(request.exam_path, Config.exam_storage.answer_key_filename)

    @staticmethod
    def _mark_detection(file_path: str, file_name: str):
        image = Storage.get_exam_image(file_path, file_name)
        answer_input, index_input = Preprocessing().process(image)
        index_result = IndexModel(Config.paths.index_model_path).inference(index_input)
        logging.info(f"Detected index: {index_result}")
        answer_result = AnswerModel(Config.paths.answer_model_path).inference(answer_input)
        logging.info(f"Detected answers: {Controller._get_readable_answers(answer_result)}")
        json_result = Controller._create_output_json(answer_result, index_result)
        output_file = file_name.split('.')[0]
        Storage.set_exam_answer_json(file_path, output_file, json_result)

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
