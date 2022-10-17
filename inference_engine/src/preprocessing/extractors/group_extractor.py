from .extractor import Extractor
from src.config import Config

import cv2
import numpy as np


class GroupExtractor(Extractor):
    def process(self, *args, **kwargs):
        self.remove_borders(15)
        rectangles = self.detect_rectangles()
        x, y, w, h = max(rectangles, key=lambda x: x[2] * x[3])
        crop = self._operated_img[y:y + h, x:x + w].copy()
        row = cv2.resize(crop, Config.inference.answer_row_shape)
        row = cv2.merge([row] * 3)
        row = np.expand_dims(row, 0)
        return row
