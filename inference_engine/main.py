import logging

from src.controller import Controller
from src.dto import CheckExamDTO, CheckExamsDTO, GenerateExamKeyDTO

logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    Controller.generate_exam_key(GenerateExamKeyDTO.parse_obj({'exam_path': 'subject'}))
    Controller.check_exam(CheckExamDTO.parse_obj({'exam_path': 'subject', 'exam_name': 'image--001.jpg'}))
    Controller.check_exams(CheckExamsDTO.parse_obj({'exam_path': 'subject'}))
