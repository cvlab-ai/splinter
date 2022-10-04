from fastapi import APIRouter

from .dto import CheckExamDTO, CheckExamsDTO, GenerateExamKeyDTO
from .controller import Controller

router = APIRouter()


@router.get("/")
def test():
    return "TEST"


@router.post("/check-exam")
def check_exam(check_exam_dto: CheckExamDTO):
    Controller.check_exam(check_exam_dto)
    return "Success!"


@router.post("/check-exams")
def check_exam(check_exam_dto: CheckExamsDTO):
    Controller.check_exams(check_exam_dto)
    return "Success!"


@router.post("/generate-exam-key")
def generate_exam_key(generate_exam_key_dto: GenerateExamKeyDTO):
    Controller.generate_exam_key(generate_exam_key_dto)
    return "Success!"
