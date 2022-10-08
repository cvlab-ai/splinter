import logging

from src.controller import Controller
from src.dto import CheckExamDTO, CheckExamsDTO

logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    Controller.check_exams(CheckExamsDTO.parse_obj({'exam_path': 'exams'}))
    # Controller.check_exam(CheckExamDTO.parse_obj({'exam_path': 'exams', 'exam_name': 'image--001.jpg'}))
