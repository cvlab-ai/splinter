import itertools
import typing as tp

import numpy as np

from .index_extraction import IndexExtraction
from .help import *
from .fields import Fields


class Preprocessing:
    def __init__(self, image: np.ndarray, binary_threshold: int = 185, expected_shape: tuple = (290, 60)):
        self.image = image.copy()
        self.binary_threshold = binary_threshold
        self.expected_shape = expected_shape

    def process(self) -> tp.Tuple[np.ndarray, np.ndarray]:
        operated_image = self.prepare_image(self.image)
        box_images = self.separate_content_boxes(operated_image)
        index_img = IndexExtraction(box_images[Fields.student_id]).extract()
        box_positions = self._detect_box_positions(box_images[Fields.answers])
        print(box_positions)
        cropped_rows = self.crop_rows(box_images[Fields.answers], box_positions)
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
        raise NotImplementedError
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
    def separate_content_boxes(image: np.ndarray, y_disc: int = 10) -> tp.Dict[Fields, np.ndarray]:
        image_copy = image.copy()
        contours = detect_contours(image_copy)
        grouped_contours = group_by_size(contours)
        grouped_contours = Preprocessing.unpack_broad_groups(grouped_contours)
        rectangles = [calculate_rectangle(contour, inside=False) for contour in grouped_contours]
        rectangles = Preprocessing.remove_broad_rectangles(rectangles)
        sorted_rectangles = sorted(rectangles, key=lambda x: (int(x[1]/y_disc), x[0]))
        box_images = []
        for x, y, w, h in sorted_rectangles:
            box_images.append(image_copy[y:y + h, x:x + w].copy())
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
