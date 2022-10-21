import logging

from .storage import Storage
from .dto import CheckPdfDTO, CheckExamDTO, GenerateExamKeysDTO
from .exam import exam
from .pdf import PDFType

class Controller:
    @staticmethod
    def check_pdf(request: CheckPdfDTO):
        exam.check_pdf(request.exam_id,request.file_name, PDFType.answer_sheets, request.force)

    @staticmethod
    def check_exam(request: CheckExamDTO):
        logging.info(f"Checking exam: {request.exam_id}")
        files = Storage.get_pdfs_names(request.exam_id, PDFType.answer_sheets)
        if files is None:
            return
        for file_name in files:
            logging.info(f"Checking answer pdf: {file_name}")
            exam.check_pdf(request.exam_id, file_name, PDFType.answer_sheets, request.force)

    @staticmethod
    def generate_exam_keys(request: GenerateExamKeysDTO):
        logging.info(f"Generating answer keys for exam: {request.exam_id}")
        files = Storage.get_pdfs_names(request.exam_id, PDFType.answer_keys)
        if files is None:
            return
        for file_name in files:
            logging.info(f"Checking answer key pdf: {file_name}")
            exam.check_pdf(request.exam_id, file_name, PDFType.answer_keys, request.force)

