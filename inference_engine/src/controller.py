from src.config import Config
from .exam_storage import ExamStorage
from .inferenece_runner import InferenceModel
from .dto import CheckExamsDTO, CheckExamDTO, GenerateExamKeyDTO


class Controller:
    @staticmethod
    def check_exam(request: CheckExamDTO):
        return Controller._mark_detection(request.exam_path, request.exam_name)

    @staticmethod
    def check_exams(request: CheckExamsDTO):
        for exam_name in ExamStorage.get_exams_names(request.exam_path):
            Controller._mark_detection(request.exam_path, exam_name)

    @staticmethod
    def generate_exam_key(request: GenerateExamKeyDTO):
        return Controller._mark_detection(request.exam_path, Config.exam_storage.answer_key_filename)

    @staticmethod
    def _mark_detection(file_path: str, file_name: str):
        image = ExamStorage.get_exam_image(file_path, file_name)
        inference_model = InferenceModel()
        result = inference_model.run_inference(image)
        return result
