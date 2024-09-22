import typing as tp

import cv2
import numpy as np

from .help import read_image, detect_contours, detect_lines, group_by_size, calculate_rectangle, detect_boxes_middles
import os

class ExamSolver:
    def __init__(self, image_path: str):
        self._image_path = image_path
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File {image_path} not found")

        self.image = read_image(image_path)
        self.answer_card = None
        self.box_positions = None
        self.box_shape = None

        self._detect_answer_card()
        self._detect_box_positions()

    def _detect_answer_card(self):
        contours = detect_contours(image=self.image)

        grouped_rectangle_contours = group_by_size(contours)[0]
        rectangle_answers_connected = calculate_rectangle(grouped_rectangle_contours, inside=False)

        x1, y1, w1, h1 = rectangle_answers_connected[0]
        answers_image = self.image[y1:y1 + h1, x1:x1 + w1]

        answers_image[answers_image <= 170] = 0
        answers_image[answers_image > 170] = 255
        self.answer_card = answers_image

    def _detect_box_positions(self):
        thresh = cv2.threshold(self.answer_card, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        horizontal_contours = detect_lines(thresh, (40, 1))
        vertical_contours = detect_lines(thresh, (1, 30))
        self._detect_box_shape(vertical_contours)
        self.box_positions = self._group_box_positions(horizontal_contours, vertical_contours)

    def _group_box_positions(self, horizontal_contours: np.ndarray, vertical_contours: np.ndarray):
        grouped_box_positions = []
        grouped_vertical_contours = self._group_by(vertical_contours, lambda x: x[0][0], 2)
        for column_vertical in grouped_vertical_contours:
            box_positions = detect_boxes_middles(horizontal_contours, column_vertical)
            grouped_boxes_in_row = self._group_by(box_positions, lambda x: x[1], int(len(box_positions) / 4))
            grouped_box_positions.extend(grouped_boxes_in_row)
        return np.array(grouped_box_positions)
        
    @staticmethod
    def _group_by(data: np.ndarray, sort_func: tp.Callable, number_of_groups: int):
        return np.array_split(sorted(data, key=sort_func), number_of_groups)

    def _detect_box_shape(self, vertical_contours: np.ndarray):
        vertical_deltas = [v1[0][0] - v2[0][0] for v1, v2 in zip(vertical_contours[:-1], vertical_contours[1:])]
        vertical_median = np.median(vertical_deltas) * 0.7
        self.box_shape = np.array([vertical_median, vertical_median], dtype=np.uint8)

    def get_answer_card(self):
        return cv2.cvtColor(self.answer_card, cv2.COLOR_GRAY2RGB)
