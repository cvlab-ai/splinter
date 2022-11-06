import typing as tp
import itertools

import numpy as np

from src.preprocessing import Fields
from .extractor import Extractor


class FieldExtractor(Extractor):
    def process(self, *args, **kwargs):
        self.to_portrait()
        self.to_grayscale()
        saved_extractor = Extractor(self._operated_img)

        self.to_binary(180)
        rectangles = self.detect_rectangles()
        rectangles = self._remove_rectangles_by_size(rectangles)
        sorted_rectangles = sorted(rectangles, key=lambda x: (int(x[1] / 10), x[0]))

        box_images = saved_extractor.extract(sorted_rectangles)
        assigned_box_images = self._assign_field_names(box_images)
        return assigned_box_images

    def detect_rectangles(self):
        contours = self.detect_contours()
        grouped_contours = self.group_by_size(contours)
        grouped_contours = self._remove_contours_by_size(grouped_contours)
        grouped_contours = self._unpack_groups(grouped_contours, min_area_to_unpack=30000)
        return [self.calculate_rectangle(contour, inside=False) for contour in grouped_contours]

    @staticmethod
    def _assign_field_names(box_images: tp.List[np.ndarray]):
        return [(field, image) for field, image in zip(Fields.multiplied_answer_columns(), box_images)]

    @staticmethod
    def _unpack_groups(groups: tp.Dict[float, tp.List], min_area_to_unpack: float = 5000):
        def _unpack(_group):
            return [[elem] for elem in _group]
        return list(itertools.chain(*[_unpack(g) if a > min_area_to_unpack else [g] for a, g in groups.items()]))

    @staticmethod
    def _remove_rectangles_by_size(rectangles, min_area: float = 1000, max_area: float = 1000000):
        return [r for r in rectangles if min_area < r[2] * r[3] < max_area]

    @staticmethod
    def _remove_contours_by_size(grouped_contours, min_area: float = 5000, max_area: float = 1000000):
        return {area: contours for area, contours in grouped_contours.items() if min_area < area < max_area}
