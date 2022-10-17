import logging
import typing as tp

import numpy as np
import cv2

from .extractor import Extractor
from src.config import Config


class RowsExtractor(Extractor):

    def process(self):
        rows = []
        for i, column in enumerate(self._extract_columns(Config.exam.number_of_columns)):
            new_rows = self._extract_rows(column)
            rows.extend(new_rows)
            logging.info(f"Detected {len(new_rows)} answer rows in column {i + 1}")
        return np.array(rows)

    def _extract_columns(self, number_of_columns: int):
        columns = []
        for column_split in self.split_vertically(number_of_columns):
            column_extractor = Extractor(column_split)
            column_extractor.erode((3, 3))
            rectangles = column_extractor.detect_rectangles()
            x, y, w, h = max(rectangles, key=lambda _x: _x[2] * _x[3])
            columns.append(column_split[y:y + h, x:x + w])
        return columns

    def _extract_rows(self, column: np.ndarray, height_similarity: float = 0.1):
        rows_extractor = Extractor(column)
        rows_extractor.erode((3, 3))
        horizontal_lines = np.array(sorted(rows_extractor.detect_lines((60, 1)), key=lambda x: x[0][1]))
        y_values = list(horizontal_lines[:, 0, 1])
        y_values = self.fill_missing_values(y_values, column.shape[0], 10)
        row_median_height = self.__calculate_row_height(y_values)

        rows = []
        for y1, y2 in zip(y_values[:-1], y_values[1:]):
            if abs(((y2 - y1) / row_median_height) - 1) < height_similarity:
                row = column[y1:y2, :]
                row = cv2.resize(row, Config.inference.answer_row_shape)
                row = cv2.merge([row] * 3)
                rows.append(row)
        return rows

    @staticmethod
    def fill_missing_values(y_values: tp.List[int], y_column: int, threshold: 5):
        if y_values[0] > threshold:
            y_values.insert(0, 0)
        if y_column - y_values[-1] > threshold:
            y_values.append(y_column)
        return y_values

    @staticmethod
    def __calculate_row_height(y_values: tp.List[int]):
        roll_rows_y = np.roll(y_values, 1)
        roll_rows_y[0] = 0
        return float(np.median(y_values - roll_rows_y))
