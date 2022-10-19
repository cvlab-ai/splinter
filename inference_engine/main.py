import logging

from src.controller import Controller
from src.storage import Storage
from src.dto import CheckExamDTO, CheckPdfDTO, GenerateExamKeysDTO

logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    # Controller.check_pdf(CheckExamDTO.parse_obj({'exam_path': 'subject', 'exam_name': 'image--001.jpg'}))
    # Controller.check_exam(CheckPdfDTO.parse_obj({'exam_path': 'subject'}))
    # Controller.generate_exam_keys(GenerateExamKeysDTO.parse_obj({'exam_path': 'subject'}))
    print(Storage.next_answer_version(1, 1234))
    Controller.check_pdf(CheckPdfDTO.parse_obj({'exam_id': '1', 'file_name' : 'test.pdf'}))

