import itertools
import logging

from .index_extractor import IndexExtractor
from .rows_extractor import RowsExtractor
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
        index_img = IndexExtractor(box_images[Fields.student_id]).process()
        rows_img = RowsExtractor(box_images[Fields.answers]).process(3)
        logging.info(f"Detected {rows_img.shape[0]} answer rows")
        return rows_img, index_img

    def prepare_image(self, image: np.ndarray) -> np.ndarray:
        image = image.copy()
        image = to_grayscale(image)
        image = to_binary(image, self.binary_threshold)
        image = to_portrait(image)
        return image

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
