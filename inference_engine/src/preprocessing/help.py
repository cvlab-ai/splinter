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


def to_grayscale(image: np.ndarray) -> np.ndarray:
    if image.shape[-1] > 1:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def to_binary(image: np.ndarray, threshold) -> np.ndarray:
    image[image <= threshold] = 0
    image[image > threshold] = 255
    return image


def to_portrait(image: np.ndarray) -> np.ndarray:
    if image.shape[0] < image.shape[1]:
        return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return image


def detect_contours(image: np.ndarray, threshold: int = 80) -> np.ndarray:
    new_image = image.copy()
    lower_black = np.array([0])
    upper_black = np.array([threshold])
    mask = cv2.inRange(new_image, lowerb=lower_black, upperb=upper_black)
    black_cnt = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]
    return black_cnt


def group_by_size(contours: np.ndarray, similarity_prop: float = 1.1, dropout: int = 600) -> tp.Dict[float, tp.List[int]]:
    groups = defaultdict(list)
    contours = drop_insignificant(contours, dropout=dropout)

    def find_group(c_area: int):
        return next((g_area for g_area in groups.keys() if g_area / c_area < similarity_prop), None)

    for contour in sorted(contours, key=cv2.contourArea, reverse=True):
        contour_area = cv2.contourArea(contour)
        if (group_area := find_group(contour_area)) is not None:
            groups[group_area].append(contour)  # Add contour to existing found group
        else:
            groups[contour_area].append(contour)  # Create new group with contour area as key
    return dict(groups)


def drop_insignificant(contours: np.ndarray, dropout: int):
    return [contour for contour in contours if cv2.contourArea(contour) >= dropout]


def mark_contours(
    image: np.ndarray, contours: np.ndarray, frame_color: Tuple[int] = (0, 255, 0)
) -> np.ndarray:
    if len(image.shape) == 2:
        new_image = cv2.cvtColor(image.copy(), cv2.COLOR_GRAY2RGB)
    else:
        new_image = image.copy()
    for m_area in contours:
        if type(m_area[0]) != int:
            (xg, yg, wg, hg) = cv2.boundingRect(m_area)
        else:
            (xg, yg, wg, hg) = m_area
        cv2.rectangle(new_image, (xg, yg), (xg + wg, yg + hg), frame_color, 2)
    return new_image


def mark_squares_on_image(image: np.ndarray, coordinates: List[List[int]]):
    fig, ax = plt.subplots()
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    ax.imshow(image)
    for (x1, y1, w1, h1) in coordinates:
        color = choice(list(mcolors.CSS4_COLORS.keys()))
        rect = Rectangle((x1, y1), w1, h1, linewidth=2, edgecolor=color, facecolor='none')
        ax.add_patch(rect)
    plt.show()


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


def detect_lines(threshold, kernel_size: Tuple[int, int]):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    detect = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel, iterations=2)
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
