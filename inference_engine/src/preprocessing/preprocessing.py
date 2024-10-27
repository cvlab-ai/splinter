import logging
import typing as tp
from collections import defaultdict
from PIL import Image

import numpy as np
import cv2

from src.utils.exceptions import PreprocessingError
from .extractors import TextExtractor, IndexExtractor, BoxExtractor, FieldExtractor, GroupExtractor
from .fields import FieldName, Field
from .rotation import rotate_exam


class Preprocessing:
    FIELD_EXTRACTOR_MAPPING = {
        FieldName.exam_title: TextExtractor,
        FieldName.student_name: TextExtractor,
        FieldName.date: TextExtractor,
        FieldName.exam_key: GroupExtractor,
        FieldName.student_id: IndexExtractor,
        FieldName.answers: BoxExtractor
    }

    def __init__(self, img: np.ndarray):
        self._exam_copy = img.copy()

    def process(self) -> tp.Tuple[tp.Dict[FieldName, tp.List[Field]], np.ndarray]:
        self.show_image(self._exam_copy)
        # self._exam_copy = rotate_exam(self._exam_copy) # Preprocessing do wywalenia (rotate xam
        # self.show_image(self._exam_copy)
        try:
            fields = FieldExtractor(Field(self._exam_copy)).process() # TODO Przeorbić field Extractor (na podstawie px)
            _map = Preprocessing.FIELD_EXTRACTOR_MAPPING
            result = [(name, _map[name](field).process()) for name, field in fields if name in _map]
            result = self.group_by_field(result)
        except (IndexError, ValueError, cv2.error) as e:
            logging.exception(e)
            raise PreprocessingError(e)
        return result, self._exam_copy


    @staticmethod
    def show_image(image: np.ndarray):
        pil_image = Image.fromarray(image)
        pil_image.show()

    @staticmethod
    def group_by_field(field_images: tp.List[tp.Tuple[FieldName, np.ndarray]]) -> tp.Dict[FieldName, tp.List[Field]]:
        grouped = defaultdict(list)
        for fieldname, field in field_images:
            grouped[fieldname].append(field)
        return dict(grouped)
