import random
import typing as tp
from pathlib import Path

import cv2
import numpy as np

from research.data_augmentator import DataAugmentator
from research.mark_generator import MarkGenerator, Mark


class TrainingDataGenerator:
    ANSWER_BOXES_PATH = 'data/input/answer_boxes.jpg'
    INDEX_BOXES_PATH = 'data/input/index_boxes.jpg'
    OUTPUT_DIR = 'data/output'

    def __init__(self, shape: tp.Tuple = (90, 90), box_offset: int = 4):
        self._border = 5
        self._shape = shape
        self._box_offset = box_offset
        self._raw_answer_boxes = self.extract_boxes()
        self._mark_generator = self.set_mark_generator()

    def set_mark_generator(self):
        mark, unmark = Mark.get_random_valid_marks()
        alpha = random.uniform(0.05, 0.2)
        beta = random.uniform(0.05, 0.2)
        gamma = random.uniform(0.05, 0.2)
        rho = random.uniform(0.05, 0.2)
        weight = (random.randint(3, 8), random.randint(3, 8))
        return MarkGenerator(self._shape, mark, unmark, alpha, beta, gamma, rho, weight)

    def generator(self, idx: int = 0, augmentation: bool = True):
        Path(self.OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
        while True:
            marked_box, label = self.create_marked_box()
            if augmentation:
                marked_box = DataAugmentator(marked_box).gaussian_noise().shift().get()
            box_dir = f"{self.OUTPUT_DIR}/{str(idx).rjust(6, '0')}.jpg"
            cv2.imwrite(box_dir, marked_box)
            idx += 1
            yield box_dir, label

    def create_marked_box(self):
        box = random.choice(self._raw_answer_boxes)
        mark_functions = [(self._mark_generator.generate_mark, 1),
                          (self._mark_generator.generate_unmark, 0),
                          (lambda: np.zeros(self._shape, dtype=np.uint8), 0)]

        mark_func, label = random.choice(mark_functions)
        marked_box = cv2.subtract(box, mark_func())
        marked_box[marked_box < 0] = 0
        return marked_box, label

    def extract_boxes(self):
        answer_boxes = self._extract_boxes(self.ANSWER_BOXES_PATH, 4, 10)
        index_image = self._extract_boxes(self.INDEX_BOXES_PATH, 6, 10)
        return answer_boxes + index_image

    def _extract_boxes(self, path: str, x: int, y: int):
        boxes = []
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        x_parts = np.linspace(0., img.shape[1] - 2 * self._border, x + 1) + self._border
        y_parts = np.linspace(0., img.shape[0] - 2 * self._border, y + 1) + self._border
        for y0, y1 in zip(y_parts[:-1], y_parts[1:]):
            for x0, x1 in zip(x_parts[:-1], x_parts[1:]):
                box = img[int(y0) - self._box_offset: int(y1) + self._box_offset,
                          int(x0) - self._box_offset: int(x1) + self._box_offset]
                boxes.append(cv2.resize(box, dsize=self._shape))
        return boxes


if __name__ == '__main__':
    for i, (img_dir, _label) in enumerate(TrainingDataGenerator(box_offset=3).generator()):
        print(img_dir, _label)
        if i == 10:
            break
