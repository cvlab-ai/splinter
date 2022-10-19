from fastapi import APIRouter

from .dto import CheckExamDTO, CheckPdfDTO, GenerateExamKeysDTO
from .controller import Controller

router = APIRouter()


@router.get("/")
def test():
    return "TEST"


@router.post("/check-exam")
def check_exam(check_exam_dto: CheckExamDTO):
    """
    Check all pdfs in the given exam, pdfs which were already checked will not be rechecked
    Can accept force flag to ignore previous checks and recheck all uploaded pdfs.
    """
    Controller.check_exam(check_exam_dto)

@router.post("/check-pdf")
def check_pdf(check_exam_dto: CheckPdfDTO):
    """
    Check one given pdf name, if the pdf was already checked it will not recheck it unless the force flag was passed.
    """
    Controller.check_pdf(check_exam_dto)


@router.post("/generate-exam-keys")
def generate_exam_keys(generate_exam_key_dto: GenerateExamKeysDTO):
    """
    Go to anwers_keys, check all uploaded pdfs there, and treat them as correct answers keys for the given exam
    If uploaded pdfs contain duplicates, it will create a file in the following convention: answer_key_<group>_occurence.json
    Can accept force flag to ignore previous checks and recheck all uploaded pdfs.
    """
    Controller.generate_exam_keys(generate_exam_key_dto)
