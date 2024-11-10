import logging
import typing as tp

import cv2
import numpy as np

from src.utils.exceptions import PreprocessingError
from .crop import crop_exam
from .extractors import (
    FieldExtractor,
    TextExtractor,
    GroupExtractor,
    StudentIdGridExtractor,
    StudentIdTextExtractor,
    BoxExtractor,
)
from .fields import FieldName, Field
from .rotation import rotate_exam


class Preprocessing:
    FIELD_EXTRACTOR_MAPPING = {
        FieldName.EXAM_TITLE: TextExtractor,
        FieldName.STUDENT_NAME: TextExtractor,
        FieldName.DATE: TextExtractor,
        FieldName.EXAM_KEY: GroupExtractor,
        FieldName.STUDENT_ID_GRID: StudentIdGridExtractor,
        FieldName.STUDENT_ID_TEXT: StudentIdTextExtractor,
        FieldName.ANSWERS: BoxExtractor
    }

    def __init__(self, img: np.ndarray):
        self._exam_copy = img.copy()

    def process(self) -> tp.Tuple[tp.Dict[FieldName, tp.List[Field]], np.ndarray]:
        try:
            self._exam_copy = rotate_exam(self._exam_copy)
            self._exam_copy = crop_exam(self._exam_copy)
            self._exam_copy = cv2.resize(self._exam_copy, (2480, 3508))
            field_regions = FieldExtractor(Field(self._exam_copy)).process()

            result = {
                name: [self.FIELD_EXTRACTOR_MAPPING[name](field).process() for field in fields]
                for name, fields in field_regions.items()
                if name in self.FIELD_EXTRACTOR_MAPPING
            }

        except (IndexError, ValueError, cv2.error) as e:
            logging.exception(f"An error occurred during preprocessing: {e}")
            raise PreprocessingError(e)

        return result, self._exam_copy
