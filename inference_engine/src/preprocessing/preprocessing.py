import typing as tp

import numpy as np

from .index_extraction import IndexExtraction
from .help import *


class Preprocessing:
    def __init__(self, binary_threshold: int = 185, expected_shape: tuple = (290, 60)):
        self.binary_threshold = binary_threshold
        self.expected_shape = expected_shape

    def process(self, image: np.ndarray) -> tp.Tuple[np.ndarray, np.ndarray]:
        operated_image = self.prepare_image(image)
        answer_card, personal_info = self.separate_answer_from_top(operated_image)
        index_img = IndexExtraction(personal_info).extract()
        box_positions = self._detect_box_positions(answer_card)
        cropped_rows = self.crop_rows(answer_card, box_positions)
        return cropped_rows, index_img

    def crop_rows(self, answer_card: np.ndarray, box_positions: np.ndarray):
        def shift_each_box(box):
            x1 = box[0][0] - x_shift
            x2 = box[-1][0] + x_shift
            y1 = box[0][1] - y_shift
            y2 = box[0][1] + y_shift
            return y1, y2, x1, x2

        def crop_image(box):
            y1, y2, x1, x2 = box
            _img = cv2.resize(answer_card[y1:y2, x1:x2], self.expected_shape)
            return cv2.merge([_img] * 3)  # For some reason model has three channel input for grayscale images

        x_shift = (box_positions[0][-1][0] - box_positions[0][0][0]) // ((box_positions.shape[1] - 1) * 2)
        y_shift = (box_positions[1][0][1] - box_positions[0][0][1]) // 2
        shifted_positions = [shift_each_box(box) for box in box_positions]
        image_crops_np = np.empty((box_positions.shape[0], *self.expected_shape[::-1], 3))
        image_crops = [crop_image(positions) for positions in shifted_positions]
        for idx in range(len(image_crops_np)):
            image_crops_np[idx] = image_crops[idx]
        return image_crops_np

    def prepare_image(self, image: np.ndarray) -> np.ndarray:
        image = image.copy()
        image = to_grayscale(image)
        image = to_binary(image, self.binary_threshold)
        image = to_portrait(image)
        return image

    def _detect_box_positions(self, answer_card):
        thresh = cv2.threshold(answer_card, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        horizontal_contours = detect_lines(thresh, (40, 1))
        vertical_contours = detect_lines(thresh, (1, 30))
        box_positions = self._group_box_positions(horizontal_contours, vertical_contours)
        return box_positions

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

    @staticmethod
    def separate_answer_from_top(image: np.ndarray) -> tp.Tuple[np.ndarray, np.ndarray]:
        contours = detect_contours(image)
        grouped_rectangle_contours = group_by_size(contours)[0]
        rectangle_answers_connected = calculate_rectangle(grouped_rectangle_contours, inside=False)
        x1, y1, w1, h1 = rectangle_answers_connected[0]
        answers_image = image[y1:y1 + h1, x1:x1 + w1]
        index_image = image[:y1]  # TODO Update it to be done same way as in ipynb
        return answers_image, index_image
