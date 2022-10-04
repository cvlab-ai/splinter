import numpy as np
import cv2
from typing import List, Tuple


def detect_contours(image: np.ndarray, threshold: int = 80) -> np.ndarray:
    new_image = image.copy()
    lower_black = np.array([0])
    upper_black = np.array([threshold])
    mask = cv2.inRange(new_image, lowerb=lower_black, upperb=upper_black)
    black_cnt = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[
        -2
    ]
    return black_cnt


def group_by_size(
    contours: np.ndarray, similarity_prop: float = 1.1
) -> List[List[int]]:
    grouped = [[]]
    cont_idx, group_idx = 0, 0

    contours = drop_insignificant(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    while cont_idx < len(contours):
        if (
            len(grouped[group_idx]) == 0
            or cv2.contourArea(grouped[group_idx][0])
            / cv2.contourArea(contours[cont_idx])
            < similarity_prop
        ):
            grouped[group_idx].append(contours[cont_idx])
        else:
            grouped.append([contours[cont_idx]])
            group_idx += 1
        cont_idx += 1

    return grouped


def drop_insignificant(contours: np.ndarray, dropout: float = 400):
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


def calculate_rectangle(contours: List[int], inside: bool = True) -> List[List[int]]:
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
    return [[min(x1, x2), min(y1, y2), w, h]]


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


def detect_boxes_middles(horizontal_lines: List[np.ndarray], vertical_lines: List[np.ndarray], shift: int = 20):
    def intersect(a, b):
        # https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
        def ccw(_a, _b, _c):
            return (_c[1] - _a[1]) * (_b[0] - _a[0]) > (_b[1] - _a[1]) * (_c[0] - _a[0])
        return ccw(a[0], b[0], b[1]) != ccw(a[1], b[0], b[1]) and ccw(a[0], a[1], b[0]) != ccw(a[0], a[1], b[1])

    def find_neighbour_horizontal_line(
        _h_line: np.ndarray, _lines: List[np.ndarray], threshold: int = 5):
        for _line in _lines:
            if abs((_line - _h_line)[:, 0].mean()) < threshold:
                return _line

    def shift_line(_line: np.ndarray, _shift: int, axis: int):
        _line_copy = _line.copy()
        _line_copy[0][axis] += shift
        return _line_copy

    result = []
    sorted_horizontal_lines = sorted(horizontal_lines, key=lambda x: x[0, 1])
    sorted_vertical_line = sorted(vertical_lines, key=lambda x: x[0, 0])

    for i, h_line_1 in enumerate(sorted_horizontal_lines[:-1]):
        h_line_2 = find_neighbour_horizontal_line(
            h_line_1, sorted_horizontal_lines[i + 1 :]
        )
        if h_line_2 is None:
            continue
        for v_line_1, v_line_2 in zip(sorted_vertical_line[:-1], sorted_vertical_line[1:]):
            v_line_1_shifted = shift_line(v_line_1, shift, 1)
            v_line_2_shifted = shift_line(v_line_2, shift, 1)
            h_line_2_shifted = shift_line(h_line_2, shift, 0)
            if intersect(v_line_1_shifted, h_line_2_shifted) and intersect(v_line_2_shifted, h_line_2_shifted):

                result.extend(
                    np.array(
                        [
                            np.mean([v_line_1[0, 0], v_line_2[0, 0]], dtype=np.int),
                            np.mean([h_line_1[0, 1], h_line_2[0, 1]], dtype=np.int),
                        ]
                    ).reshape((1, 2))
                )
    return result
