import typing as tp
from enum import IntEnum, auto

import cv2
import numpy as np

from .help import create_handwritten_circle, create_handwritten_cross, create_handwritten_tick, create_handwritten_doodle, calculate_mask, show_image, rotate


class Mark(IntEnum):
    CIRCLE = 0
    CROSS = auto()
    DOODLE = auto()
    TICK = auto()


class MarkGenerator:
    def __init__(self, shape: tp.Tuple[int, int], mark: Mark, unmark: Mark,
                 alpha: float, beta: float, gamma: float, rho: float, weight: tp.Tuple[int, int] = None):

        if weight is None:
            weight_param = max((int(np.ceil(min(shape) / 15)), 2))
            weight = np.array([weight_param, weight_param])

        self.shape = np.array(shape)
        self.mark = mark
        self.unmark = unmark
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.rho = rho
        self.weight = weight

    def generate_mark(self):
        mark_mask = self._generate_mark(self.mark)
        return self.cast_to_int(mark_mask)

    def generate_unmark(self):
        mark_mask = self._generate_mark(self.mark)
        mark_mask += self._generate_mark(self.unmark)
        mark_mask[mark_mask > 1] = 1
        return self.cast_to_int(mark_mask)

    def cast_to_int(self, mask: np.ndarray):
        return (mask * 255).astype("uint8")

    def _generate_mark(self, mark: Mark):
        weight = self.weight
        if mark == Mark.CROSS:
            mask = self._generate_cross()
        elif mark == Mark.CIRCLE:
            mask = self._generate_circle()
        elif mark == Mark.DOODLE:
            mask = self._generate_doodle()
        elif mark == Mark.TICK:
            mask = self._generate_tick()
            weight += 2
        else:
            raise NotImplementedError

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, weight)
        return cv2.dilate(mask, kernel)

    def _generate_circle(self):
        x_val, y_val = create_handwritten_circle(self.alpha, self.gamma)
        return rotate(calculate_mask(x_val, y_val, self.shape), self.rho, 1)

    def _generate_cross(self):
        x_val, y_val = create_handwritten_cross(self.alpha, self.gamma)
        return rotate(calculate_mask(x_val, y_val, self.shape), self.rho, 1)

    def _generate_doodle(self):
        x_val, y_val = create_handwritten_doodle(self.alpha, self.beta, self.gamma, (0.75, 0.75))
        return calculate_mask(x_val, y_val, self.shape)

    def _generate_tick(self):
        x_val, y_val = create_handwritten_tick(self.alpha, self.beta, self.gamma)
        return rotate(calculate_mask(x_val, y_val, self.shape), 0, 1)
