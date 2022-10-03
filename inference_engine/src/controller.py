from .exam_storage import ExamStorage
from .dto import CheckExamsDTO, CheckExamDTO, GenerateExamKeyDTO


class Controller:
    @staticmethod
    def check_exam(request: CheckExamDTO):
        return Controller._check_exam(request.exam_path, request.exam_name)

    @staticmethod
    def check_exams(request: CheckExamsDTO):
        for exam_name in ExamStorage.get_exams_names(request.exam_path):
            Controller._check_exam(request.exam_path, exam_name)

    @staticmethod
    def generate_exam_key(request: GenerateExamKeyDTO):
        raise NotImplementedError

    @staticmethod
    def _check_exam(exam_path: str, exam_name: str):
        exam_image = ExamStorage.get_exam_image(exam_path, exam_name)
        raise NotImplementedError  # TODO Run inference
