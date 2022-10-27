import logging

from src.controller import Controller
from src.dto import CheckExamDTO, GenerateExamKeysDTO

logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    Controller.check_exam(CheckExamDTO.parse_obj({'exam_id': '1', 'force': 'true'}))
    Controller.generate_exam_keys(GenerateExamKeysDTO.parse_obj({'exam_id': '1', 'force': 'true'}))

