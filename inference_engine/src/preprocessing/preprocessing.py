import typing as tp
from collections import defaultdict

import numpy as np

from .extractors import TextExtractor, IndexExtractor, BoxExtractor, FieldExtractor, GroupExtractor
from .fields import Fields
from .rotation import rotate_exam


class Preprocessing:
    FIELD_EXTRACTOR_MAPPING = {
        Fields.exam_title: TextExtractor,
        Fields.student_name: TextExtractor,
        Fields.date: TextExtractor,
        Fields.exam_key: GroupExtractor,
        Fields.student_id: IndexExtractor,
        Fields.answers: BoxExtractor
    }

    def __init__(self, img: np.ndarray):
        self._exam_copy = img.copy()

    def process(self) -> tp.Dict[Fields, np.ndarray]:
        self._exam_copy = rotate_exam(self._exam_copy)
        fields = FieldExtractor(self._exam_copy).process()
        _map = Preprocessing.FIELD_EXTRACTOR_MAPPING
        result = [(f, _map[f](img).process()) for f, img in fields if f in _map]
        result = self.group_by_field(result)
        return result

    @staticmethod
    def group_by_field(field_images: tp.List[tp.Tuple[Fields, np.ndarray]]) -> tp.Dict[Fields, np.ndarray]:
        grouped = defaultdict(list)
        for field, img in field_images:
            if isinstance(img, np.ndarray) and len(img.shape) > 4:
                grouped[field].extend(img)
            else:
                grouped[field].append(img)
        return dict(grouped)
