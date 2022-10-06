import typing as tp

import numpy as np
import cv2

from .help import to_binary, detect_lines


class IndexExtraction:
    def __init__(self, personal_info: np.ndarray):
        self._personal_info = personal_info

    def extract(self):
        personal_info_copy = to_binary(self._personal_info.copy(), 10)
        thresh = cv2.threshold(personal_info_copy, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        personal_horizontal = sorted(detect_lines(thresh, (30, 1)), key=self.calculate_line_length, reverse=True)
        personal_horizontal_boxes = self.split_horizontals_to_boxes(personal_horizontal)
        boxes = [self.extract_box(personal_info_copy, box) for box in personal_horizontal_boxes]
        index_box = min(boxes, key=lambda x: x.mean())  # Take the box that has something written
        return self.recover(index_box)

    @staticmethod
    def recover(img: np.ndarray):
        kernel1 = np.ones((3, 3), np.uint8)
        return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel1)

    @staticmethod
    def extract_box(img: np.ndarray, personal_horizontal_box: tp.List[int]):
        x, y, w, h = personal_horizontal_box
        crop = img[y:y+h, x:x+w]
        thresh = cv2.threshold(crop, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        IndexExtraction.remove_lines(crop, detect_lines(thresh, (1, 24)))
        IndexExtraction.remove_lines(crop, detect_lines(thresh, (30, 1)))
        return crop

    @staticmethod
    def remove_lines(image: np.ndarray, lines: np.ndarray, color=255, width: int = 2):
        for line in lines:
            x1 = min(line, key=lambda x: x[0])[0] - width
            y1 = min(line, key=lambda x: x[1])[1] - width
            x2 = max(line, key=lambda x: x[0])[0] + width
            y2 = max(line, key=lambda x: x[1])[1] + width
            cv2.rectangle(image, (x1, y1), (x2, y2), color, -1)

    @staticmethod
    def calculate_line_length(line: np.ndarray):
        deltas = abs(line[0] - line[1])
        return max(deltas)

    @staticmethod
    def split_horizontals_to_boxes(lines: tp.List[np.ndarray]) -> tp.List[tp.List[int]]:
        boxes = []
        idx = 0
        while idx < len(lines) // 2:
            pair_of_lines = np.concatenate((lines[2 * idx], lines[2 * idx + 1]), axis=0)
            x, y, w, h = cv2.boundingRect(pair_of_lines)
            boxes.append([x, y, w, h])
            idx += 1
        return boxes
