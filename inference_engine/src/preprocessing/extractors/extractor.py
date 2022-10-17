import typing as tp
from random import choice
from collections import defaultdict

import numpy as np
import cv2
from typing import List, Tuple

import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

from matplotlib.patches import Rectangle
import matplotlib.colors as mcolors


class Extractor:
    def __init__(self, img: np.ndarray):
        self._operated_img = img.copy()
        self._original_img = img

    def process(self, *args, **kwargs):
        return self._operated_img

    # Preprocessing
    def to_grayscale(self) -> np.ndarray:
        if self._operated_img.shape[-1] > 1:
            self._operated_img = cv2.cvtColor(self._operated_img, cv2.COLOR_BGR2GRAY)
        return self

    def to_binary(self, threshold: int) -> np.ndarray:
        self._operated_img[self._operated_img <= threshold] = 0
        self._operated_img[self._operated_img > threshold] = 255
        return self

    def to_portrait(self) -> np.ndarray:
        if self._operated_img.shape[0] < self._operated_img.shape[1]:
            return cv2.rotate(self._operated_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return self

    def remove_borders(self, width: int):
        self._operated_img = self._operated_img[width: -width, width: -width]
        return self

    def erode(self, kernel: tp.Tuple[int, int]):
        kernel = np.ones(kernel, np.uint8)
        self._operated_img = cv2.erode(self._operated_img, kernel)
        return self

    def recover(self, kernel_shape: tp.Tuple[int, int] = (5, 5)):
        kernel = np.ones(kernel_shape, np.uint8)
        self._operated_img = cv2.morphologyEx(self._operated_img, cv2.MORPH_OPEN, kernel)
        return self

    def split_vertically(self, number_of_columns: int):
        width_chunk = int(self._operated_img.shape[1] / number_of_columns)
        return [self._operated_img[:, width_chunk * i: width_chunk * (i + 1)] for i in range(number_of_columns)]

    # Computer vision
    def detect_and_remove_lines(self):
        exc = Extractor(cv2.threshold(self._operated_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1])
        lines = exc.detect_lines((25, 1)) + exc.detect_lines((1, 25))
        self._remove_lines(lines)
        return self

    def _remove_lines(self, lines: tp.List[np.ndarray], color=255, width: int = 2):
        for line in lines:
            x1 = min(line, key=lambda x: x[0])[0] - width
            y1 = min(line, key=lambda x: x[1])[1] - width
            x2 = max(line, key=lambda x: x[0])[0] + width
            y2 = max(line, key=lambda x: x[1])[1] + width
            cv2.rectangle(self._operated_img, (x1, y1), (x2, y2), color, -1)
        return self

    def detect_rectangles(self):
        contours = self.detect_contours()
        grouped_contours = self._group_by_size(contours).values()
        return [self.calculate_rectangle(contour, inside=False) for contour in grouped_contours]

    def detect_contours(self, threshold: int = 80) -> np.ndarray:
        lower_black = np.array([0])
        upper_black = np.array([threshold])
        mask = cv2.inRange(self._operated_img, lowerb=lower_black, upperb=upper_black)
        black_cnt = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]
        return black_cnt

    @staticmethod
    def _group_by_size(contours: np.ndarray, similarity_prop: float = 1.1, dropout: int = 600
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
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
        detect = cv2.morphologyEx(self._operated_img, cv2.MORPH_OPEN, kernel, iterations=2)
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

    # Visualization
    def vis(self, coordinates: List[List[int]] = None, title: str = ""):
        coordinates = coordinates or []

        fig, ax = plt.subplots()
        image = cv2.cvtColor(self._operated_img, cv2.COLOR_GRAY2RGB)
        ax.imshow(image)
        for (x1, y1, w1, h1) in coordinates:
            color = choice(list(mcolors.CSS4_COLORS.keys()))
            rect = Rectangle((x1, y1), w1, h1, linewidth=2, edgecolor=color, facecolor='none')
            ax.add_patch(rect)
        plt.title(title)
        plt.show()
