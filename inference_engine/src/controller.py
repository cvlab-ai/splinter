from src.config import Config
from .storage import Storage
from .preprocessing import Preprocessing
from .model import Model, IndexModel
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
        answer_result = Model(Config.paths.answer_model_path).inference(answer_input)
        index_result = IndexModel(Config.paths.index_model_path).inference(index_input)
        return answer_result
