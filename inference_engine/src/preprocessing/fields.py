import typing as tp
from enum import Enum, auto

import numpy as np


class FieldName(Enum):
    EXAM_TITLE = auto()
    STUDENT_NAME = auto()
    DATE = auto()
    EXAM_KEY = auto()
    STUDENT_ID_GRID = auto()
    STUDENT_ID_TEXT = auto()
    ANSWERS = auto()


class Field:
    def __init__(
            self,
            img: np.ndarray,
            rect: tp.Tuple[int, int, int, int] = (0, 0, 0, 0),
            field_name: FieldName = None
    ):
        self.img = img
        self.rect = rect
        self.field_name = field_name

    def __repr__(self):
        return f"{self.rect} -> {self.img}"
