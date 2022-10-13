import typing as tp
import itertools

import numpy as np

from src.preprocessing import Fields
from .extractor import Extractor


class FieldExtractor(Extractor):
    def process(self, *args, **kwargs):
        self.to_grayscale()
        self.to_binary(185)
        self.to_portrait()

        # Calculate rectangles on erode
        mask_extractor = FieldExtractor(self._operated_img)
        mask_extractor.erode((2, 2))
        rectangles = mask_extractor.detect_rectangles()
        rectangles = mask_extractor._remove_rectangles_by_size(rectangles)
        sorted_rectangles = sorted(rectangles, key=lambda x: (int(x[1] / 10), x[0]))

        box_images = self._extract_and_remove(sorted_rectangles, 4)
        assigned_box_images = self._assign_field_names(box_images)
        return assigned_box_images

    def detect_rectangles(self):
        contours = self.detect_contours()
        grouped_contours = self._group_by_size(contours)
        grouped_contours = self._unpack_broad_groups(grouped_contours)
        return [self.calculate_rectangle(contour, inside=False) for contour in grouped_contours]

    def _extract_and_remove(self, rectangles: tp.List[tp.List[int]], b: int):
        """
        :param rectangles: position of area to extract as x, y, width, height
        :param b: borders that expand extracted area
        :return: extracted fields from operated image
        """
        fields = []
        for x, y, w, h in rectangles:
            fields.append(self._operated_img[y - b:y + h + b, x - b:x + w + b].copy())
            self._operated_img[y:y + h, x:x + w] = 255
        return fields

    @staticmethod
    def _assign_field_names(box_images: tp.List[np.ndarray]):
        return {field: image for field, image in zip(Fields, box_images)}

    @staticmethod
    def _unpack_broad_groups(groups: tp.Dict[float, tp.List], max_area: float = 5000):
        def _unpack(_group):
            return [[elem] for elem in _group]
        return list(itertools.chain(*[_unpack(g) if a > max_area else [g] for a, g in groups.items()]))

    @staticmethod
    def _remove_rectangles_by_size(rectangles, min_area: float = 10000, max_area: float = 1000000):
        return [r for r in rectangles if min_area < r[2] * r[3] < max_area]
