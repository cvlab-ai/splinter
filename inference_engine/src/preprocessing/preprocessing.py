import itertools
import typing as tp

import numpy as np

from .index_extraction import IndexExtraction
from .help import *
from .fields import Fields


class Preprocessing:
    def __init__(self, image: np.ndarray, binary_threshold: int = 185, row_shape: tuple = (290, 60)):
        self.image = image.copy()
        self.binary_threshold = binary_threshold
        self.row_shape = row_shape

    def process(self) -> tp.Tuple[np.ndarray, np.ndarray]:
        operated_image = self.prepare_image(self.image)
        box_images = self.separate_content_boxes(operated_image)
        index_img = IndexExtraction(box_images[Fields.student_id]).extract()
        rows_img = self.detect_rows(box_images[Fields.answers], 3)
        return rows_img, index_img

    def prepare_image(self, image: np.ndarray) -> np.ndarray:
        image = image.copy()
        image = to_grayscale(image)
        image = to_binary(image, self.binary_threshold)
        image = to_portrait(image)
        return image

    def detect_rows(self, answer_card: np.ndarray, number_of_columns: int):
        rows = []
        for column in self.extract_columns(answer_card, number_of_columns):
            rows.extend(self.extract_rows(column))
        return np.array(rows)

    def extract_columns(self, answer_card: np.ndarray, number_of_columns: int):
        columns = []
        for answer_card_split in self.split_verticaly(answer_card, number_of_columns):
            mask = cv2.erode(answer_card_split, np.ones((5, 5)))
            contours = detect_contours(mask)
            grouped_contours = group_by_size(contours).values()
            rectangles = [calculate_rectangle(contour, inside=False) for contour in grouped_contours]
            x, y, w, h = max(rectangles, key=lambda _x: _x[2] * _x[3])
            columns.append(answer_card_split[y:y + h, x:x + w])
        return columns

    def extract_rows(self, column: np.ndarray, height_similarity = 1.1):
        mask = cv2.erode(column, np.ones((3, 3)))
        horizontal_lines = np.array(sorted(detect_lines(mask, (60, 1)), key=lambda x: x[0][1]))
        row_median_height = self._calculate_row_height(horizontal_lines)
        rows = []
        for line1, line2 in zip(horizontal_lines[:-1], horizontal_lines[1:]):
            y1, y2 = line1[0][1], line2[0][1]
            if ((y2 - y1) / row_median_height) < height_similarity:
                row = column[y1:y2, :]
                row = cv2.resize(row, self.row_shape)
                row = cv2.merge([row] * 3)
                rows.append(row)
        return rows

    def _calculate_row_height(self, horizontal_lines: np.ndarray):
        rows_y = horizontal_lines[:, 0, 1]
        roll_rows_y = np.roll(rows_y, 1)
        roll_rows_y[0] = 0
        return float(np.median(rows_y - roll_rows_y))

    def split_verticaly(self, img: np.ndarray, number_of_columns: int):
        width_chunk = int(img.shape[1] / number_of_columns)
        return [img[:, width_chunk * i: width_chunk * (i + 1)] for i in range(number_of_columns)]

    @staticmethod
    def separate_content_boxes(image: np.ndarray, y_disc: int = 10, b: int = 2) -> tp.Dict[Fields, np.ndarray]:
        image_copy = image.copy()
        contours = detect_contours(image_copy)
        grouped_contours = group_by_size(contours)
        grouped_contours = Preprocessing.unpack_broad_groups(grouped_contours)
        rectangles = [calculate_rectangle(contour, inside=False) for contour in grouped_contours]
        rectangles = Preprocessing.remove_broad_rectangles(rectangles)
        sorted_rectangles = sorted(rectangles, key=lambda x: (int(x[1]/y_disc), x[0]))
        box_images = []
        for x, y, w, h in sorted_rectangles:
            box_images.append(image_copy[y - b:y + h + b, x - b:x + w + b].copy())
            image_copy[y:y + h, x:x + w] = 255
        # mark_squares_on_image(image, sorted_rectangles)
        assigned_box_images = Preprocessing.assign_field_names(box_images)
        return assigned_box_images

    @staticmethod
    def assign_field_names(box_images: tp.List[np.ndarray]):
        return {field: image for field, image in zip(Fields, box_images)}

    @staticmethod
    def unpack_broad_groups(groups: tp.Dict[float, tp.List], max_area: float = 5000):
        def _unpack(_group):
            return [[elem] for elem in _group]
        return list(itertools.chain(*[_unpack(g) if a > max_area else [g] for a, g in groups.items()]))

    @staticmethod
    def remove_broad_rectangles(rectangles, max_area: float = 1000000):
        return [r for r in rectangles if r[2] * r[3] < max_area]
