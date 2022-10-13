from enum import Enum


class Fields(Enum):
    exam_title = 1
    student_name = 2
    student_group = 3
    date = 4
    exam_key = 5
    student_id = 6
    answers_rows = 7

    @staticmethod
    def ocr_fields():
        return [Fields.exam_title, Fields.student_name, Fields.student_group, Fields.date, Fields.student_id]
