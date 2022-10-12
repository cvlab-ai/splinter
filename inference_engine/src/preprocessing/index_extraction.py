import typing as tp

import numpy as np
import cv2

from .help import to_binary, detect_lines, detect_contours, group_by_size, calculate_rectangle


class IndexExtraction:
    def __init__(self, index_field: np.ndarray):
        self._index_field = index_field.copy()

    def extract(self):
        self.remove_borders(5)
        self._index_field = to_binary(self._index_field, 10)
        contours = detect_contours(self._index_field)
        grouped_contours = group_by_size(contours).values()
        rectangles = [calculate_rectangle(contour, inside=False) for contour in grouped_contours]
        rectangles_by_area = sorted(rectangles, key=lambda x: x[2] * x[3])
        rectangle_images = [self._index_field[y:y + h, x:x + w] for x, y, w, h in rectangles_by_area]
        index_number_field, index_answer_field = rectangle_images
        index_number_field = self.detect_and_remove_lines(index_number_field)
        index_number_field = self.recover(index_number_field)
        return index_number_field

    def remove_borders(self, width: int):
        self._index_field = self._index_field[width: -width, width: -width]

    @staticmethod
    def recover(img: np.ndarray):
        kernel1 = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel1)

    @staticmethod
    def detect_and_remove_lines(img: np.ndarray):
        thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        IndexExtraction.remove_lines(img, detect_lines(thresh, (1, 30)))
        IndexExtraction.remove_lines(img, detect_lines(thresh, (20, 1)))
        return img

    @staticmethod
    def remove_lines(image: np.ndarray, lines: np.ndarray, color=255, width: int = 2):
        for line in lines:
            x1 = min(line, key=lambda x: x[0])[0] - width
            y1 = min(line, key=lambda x: x[1])[1] - width
            x2 = max(line, key=lambda x: x[0])[0] + width
            y2 = max(line, key=lambda x: x[1])[1] + width
            cv2.rectangle(image, (x1, y1), (x2, y2), color, -1)
