from enum import Enum
from src.config import Config


class Fields(Enum):
    exam_title = 1
    student_name = 2
    date = 3
    exam_key = 4
    student_id = 5
    answers = 6

    @staticmethod
    def ocr_fields():
        return [Fields.exam_title, Fields.student_name, Fields.date, Fields.student_id]

    @staticmethod
    def multiplied_answer_columns():
        fields = list(Fields)
        answers_idx = fields.index(Fields.answers)
        fields[answers_idx:answers_idx + 1] = [Fields.answers] * Config.exam.number_of_columns
        return fields
