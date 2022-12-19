import typing as tp

from enum import Enum

import numpy as np

from src.config import Config


class Field:
    def __init__(self, img: np.ndarray, rect: tp.Tuple[int, int, int, int] = (0, 0, 0, 0)):
        self.img = img
        self.rect = rect

    def __repr__(self):
        return f"{self.rect} -> {self.img}"


class FieldName(Enum):
    exam_title = 1
    student_name = 2
    date = 3
    exam_key = 4
    student_id = 5
    answers = 6

    @staticmethod
    def ocr_fields():
        return [FieldName.exam_title, FieldName.student_name, FieldName.date]

    @staticmethod
    def multiplied_answer_columns():
        fields = list(FieldName)
        answers_idx = fields.index(FieldName.answers)
        fields[answers_idx:answers_idx + 1] = [FieldName.answers] * Config.exam.number_of_columns
        return fields
