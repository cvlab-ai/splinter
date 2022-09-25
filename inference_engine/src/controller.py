from .dto import CheckExamsDTO, CheckExamDTO, GenerateExamKeyDTO


class Controller:
    @staticmethod
    def check_exam(request: CheckExamDTO):
        raise NotImplementedError

    @staticmethod
    def check_exams(request: CheckExamsDTO):
        raise NotImplementedError

    @staticmethod
    def generate_exam_key(request: GenerateExamKeyDTO):
        raise NotImplementedError
