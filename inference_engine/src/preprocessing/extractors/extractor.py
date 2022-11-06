from __future__ import annotations

import typing as tp
from random import choice
from collections import defaultdict

import numpy as np
import cv2
from typing import List, Tuple

import matplotlib

matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from matplotlib import collections as mc

from matplotlib.patches import Rectangle
import matplotlib.colors as mcolors


class Extractor:
    def __init__(self, img: np.ndarray):
        self._operated_img = img.copy()
        self._original_img = img

    def process(self, *args, **kwargs):
        return self._operated_img

    # Preprocessing
    def to_grayscale(self) -> Extractor:
        if len(self._operated_img.shape) > 2:
            self._operated_img = cv2.cvtColor(self._operated_img, cv2.COLOR_BGR2GRAY)
        return self

    def to_binary(self, threshold: int) -> Extractor:
        self._operated_img[self._operated_img <= threshold] = 0
        self._operated_img[self._operated_img > threshold] = 255
        return self

    def to_portrait(self) -> Extractor:
        if self._operated_img.shape[0] < self._operated_img.shape[1]:
            return cv2.rotate(self._operated_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return self

    def remove_borders(self, width: int) -> Extractor:
        self._operated_img = self._operated_img[width: -width, width: -width]
        return self

    def erode(self, kernel: tp.Tuple[int, int]) -> Extractor:
        kernel = np.ones(kernel, np.uint8)
        self._operated_img = cv2.erode(self._operated_img, kernel)
        return self

    def recover(self, kernel_shape: tp.Tuple[int, int] = (5, 5)) -> Extractor:
        kernel = np.ones(kernel_shape, np.uint8)
        self._operated_img = cv2.morphologyEx(self._operated_img, cv2.MORPH_OPEN, kernel)
        return self

    def split_vertically(self, number_of_columns: int):
        width_chunk = int(self._operated_img.shape[1] / number_of_columns)
        return [self._operated_img[:, width_chunk * i: width_chunk * (i + 1)] for i in range(number_of_columns)]

    # Computer vision
    def detect_and_remove_lines(self):
        lines = self.detect_lines((25, 1)) + self.detect_lines((1, 25))
        self.remove_lines(lines)
        return self

    def remove_lines(self, lines: tp.List[np.ndarray], color=255, width: int = 3):
        for line in lines:
            x1 = min(line, key=lambda x: x[0])[0] - width
            y1 = min(line, key=lambda x: x[1])[1] - width
            x2 = max(line, key=lambda x: x[0])[0] + width
            y2 = max(line, key=lambda x: x[1])[1] + width
            cv2.rectangle(self._operated_img, (x1, y1), (x2, y2), color, -1)
        return self

    def detect_rectangles(self):
        contours = self.detect_contours()
        grouped_contours = self.group_by_size(contours).values()
        return [self.calculate_rectangle(contour, inside=False) for contour in grouped_contours]

    def detect_contours(self, threshold: int = 80) -> np.ndarray:
        lower_black = np.array([0])
        upper_black = np.array([threshold])
        mask = cv2.inRange(self._operated_img, lowerb=lower_black, upperb=upper_black)
        black_cnt = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]
        return black_cnt

    @staticmethod
    def group_by_size(contours: np.ndarray, similarity_prop: float = 1.1, dropout: int = 600
                      ) -> tp.Dict[float, tp.List[int]]:

        def drop_insignificant(contours: np.ndarray, dropout: int):
            return [contour for contour in contours if cv2.contourArea(contour) >= dropout]

        def find_group(c_area: int, _groups: tp.Dict):
            return next((g_area for g_area in _groups.keys() if g_area / c_area < similarity_prop), None)

        groups = defaultdict(list)
        contours = drop_insignificant(contours, dropout=dropout)

        for contour in sorted(contours, key=cv2.contourArea, reverse=True):
            contour_area = cv2.contourArea(contour)
            if (group_area := find_group(contour_area, groups)) is not None:
                groups[group_area].append(contour)  # Add contour to existing found group
            else:
                groups[contour_area].append(contour)  # Create new group with contour area as key
        return dict(groups)

    @staticmethod
    def calculate_rectangle(contours: List[int], inside: bool = True) -> List[int]:
        contours = [cv2.boundingRect(contour) for contour in contours]
        right_x = [x[0] + x[2] for x in contours]
        bottom_y = [x[1] + x[3] for x in contours]
        if inside:
            first_fun, second_fun = max, min
        else:
            first_fun, second_fun = min, max
        x1 = first_fun(contours, key=lambda x: x[0])[0]
        y1 = first_fun(contours, key=lambda x: x[1])[1]

        x2 = second_fun(right_x)
        y2 = second_fun(bottom_y)
        w, h = abs(x1 - x2), abs(y1 - y2)
        return [min(x1, x2), min(y1, y2), w, h]

    def detect_lines(self, kernel_size: Tuple[int, int]):
        negative = cv2.threshold(self._operated_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
        detect = cv2.morphologyEx(negative, cv2.MORPH_OPEN, kernel, iterations=2)
        contours = cv2.findContours(detect, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours: np.ndarray = contours[0] if len(contours) == 2 else contours[1]
        lines = []
        for contour in contours:
            contour = contour.reshape((contour.shape[0], 2))
            if kernel_size[0] > kernel_size[1]:  # Detect horizontal lines
                y_mean = int(contour.mean(axis=0)[1])
                lines.append(
                    np.array(
                        [[contour.min(axis=0)[0], y_mean], [contour.max(axis=0)[0], y_mean]]
                    )
                )
            else:  # Detect vertical lines
                x_mean = int(contour.mean(axis=0)[0])
                lines.append(
                    np.array(
                        [[x_mean, contour.min(axis=0)[1]], [x_mean, contour.max(axis=0)[1]]]
                    )
                )
        return lines

    def extract(self, rectangles: tp.List[tp.List[int]]):
        """
        :param rectangles: position of area to extract as x, y, width, height
        :return: extracted fields from operated image
        """
        return [self._operated_img[y:y + h, x:x + w] for x, y, w, h in rectangles]

    @staticmethod
    def ensure_correct_distribution(values: tp.List[int], similarity: float = 0.3):
        _roll_values = np.roll(values, 1)
        _roll_values[0] = 0
        median_delta = float(np.median(values - _roll_values))

        result = [values[0]] if values else []
        for v1, v2 in zip(values[:-1], values[1:]):
            if abs(((v2 - v1) / median_delta) - 1) < similarity:
                result.append(v2)
        return result

    @staticmethod
    def fill_missing_values(values: tp.List[int], overall_size: int, threshold: int = 5):
        if values[0] > threshold:
            values.insert(0, 0)
        if overall_size - values[-1] > threshold:
            values.append(overall_size)
        return values

    # Visualization
    def vis(self, rectangles: List[List[int]] = None, lines: List[List[int]] = None, title: str = ""):
        rectangles = rectangles or []
        lines = lines or []

        fig, ax = plt.subplots()
        image = cv2.cvtColor(self._operated_img, cv2.COLOR_GRAY2RGB)
        ax.imshow(image)
        for (x1, y1, w1, h1) in rectangles:
            color = choice(list(mcolors.CSS4_COLORS.keys()))
            rect = Rectangle((x1, y1), w1, h1, linewidth=2, edgecolor=color, facecolor='none')
            ax.add_patch(rect)

        lc = mc.LineCollection(lines, linewidths=2)
        ax.add_collection(lc)
        plt.title(title)
        plt.show()

    def split_image_into_squares(self, x_squares: int, y_squares: int, group_by: str = 'y',
                                 expected_box_shape: tuple = (90, 90)):
        assert len(self._operated_img.shape) == 2
        assert group_by in ('x', 'y')
        expected_y_box, expected_x_box = expected_box_shape
        source_image = cv2.resize(self._operated_img, (expected_x_box * x_squares, expected_y_box * y_squares),
                                  interpolation=cv2.INTER_LINEAR)
        source_image = cv2.merge([source_image] * 3)
        new_y_size, new_x_size, channels = source_image.shape
        y_box_size, x_box_size = new_y_size // y_squares, new_x_size // x_squares
        assert x_box_size == expected_x_box and y_box_size == expected_y_box and channels == 3

        y_values = np.linspace(0, new_y_size, y_squares + 1, dtype=int)
        x_values = np.linspace(0, new_x_size, x_squares + 1, dtype=int)

        if group_by == 'y':
            boxes = np.array([[
                source_image[y0: y1, x0: x1]
                for x0, x1 in zip(x_values[:-1], x_values[1:])]
                for y0, y1 in zip(y_values[:-1], y_values[1:])])
            assert boxes.shape == (y_squares, x_squares, *expected_box_shape, 3)
        else:  # group_by == 'x'
            boxes = np.array([[
                source_image[y0: y1, x0: x1]
                for y0, y1 in zip(y_values[:-1], y_values[1:])]
                for x0, x1 in zip(x_values[:-1], x_values[1:])])
            assert boxes.shape == (x_squares, y_squares, *expected_box_shape, 3)
        return boxes
