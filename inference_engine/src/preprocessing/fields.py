import typing as tp
from enum import Enum, auto

import numpy as np
from PIL import Image

from src.config import Config


class FieldName(Enum):
    EXAM_TITLE = auto()
    STUDENT_NAME = auto()
    DATE = auto()
    EXAM_KEY = auto()
    STUDENT_ID_GRID = auto()
    STUDENT_ID_TEXT = auto()
    ANSWERS = auto()

    @staticmethod
    def ocr_fields():
        return [FieldName.EXAM_TITLE, FieldName.STUDENT_NAME, FieldName.DATE]

    @staticmethod
    def multiplied_answer_columns():
        fields = list(FieldName)
        answers_idx = fields.index(FieldName.ANSWERS)
        fields[answers_idx:answers_idx + 1] = [FieldName.ANSWERS] * Config.exam.number_of_columns
        return fields


class Field:
    def __init__(self, img: np.ndarray, rect: tp.Tuple[int, int, int, int] = (0, 0, 0, 0),
                 field_name: FieldName = None):
        self.img = img
        self.rect = rect
        self.field_name = field_name

    def show(self):
        Image.fromarray(self.img).show()

    def __repr__(self):
        return f"{self.rect} -> {self.img}"
