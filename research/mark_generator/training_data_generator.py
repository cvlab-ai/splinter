import logging
import random
import typing as tp
from pathlib import Path
from collections import defaultdict

import cv2
import math
import numpy as np
import os

import tqdm


from research.data_augmentator import DataAugmentator
from research.mark_generator import MarkGenerator, Mark


class TrainingDataGenerator:
    ANSWER_BOXES_PATH = os.path.join(os.path.dirname(__file__), 'data/input/answer_boxes.jpg')
    INDEX_BOXES_PATH = os.path.join(os.path.dirname(__file__), 'data/input/index_boxes.jpg')

    def __init__(self, shape: tp.Tuple = (90, 90), box_offset: int = 4, output_dir: str = 'data/output'):
        self._border_x = 11
        self._border_y = 22
        self._shape = shape
        self._box_offset = box_offset
        self._output_dir = output_dir
        self._raw_answer_boxes = self.extract_boxes()
        self._mark_generator = None
        self.set_random_mark_generator()

    def set_random_mark_generator(self):
        mark, unmark = Mark.get_random_valid_marks()
        alpha = random.uniform(0.05, 0.2)
        beta = random.uniform(0.05, 0.2)
        gamma = random.uniform(0.05, 0.2)
        rho = random.uniform(0.05, 0.2)
        weight = (random.randint(3, 8), random.randint(3, 8))
        self._mark_generator = MarkGenerator(self._shape, mark, unmark, alpha, beta, gamma, rho, weight)

    def generate(self, n: int, idx: int = 0, augmentation_chance: float = .5, change_mark_chance: float = .2):
        data_generator = self.generator(idx, augmentation_chance, change_mark_chance)
        data = defaultdict(list)
        for _ in tqdm.tqdm(range(n)):
            box_dir, label = next(data_generator)
            data["box_dirs"].append(box_dir)
            data["labels"].append(label)
        return data

    def generator(self, idx: int = 0, augmentation_chance: float = .5, change_mark_chance: float = .1):
        while True:
            marked_box, label = self.create_marked_box()
            if random.random() < augmentation_chance:
                marked_box = DataAugmentator(marked_box).gaussian_noise().shift().get()

            output_dir = Path(f"{self._output_dir}//{label}")
            output_dir.mkdir(parents=True, exist_ok=True)
            box_dir = f"{output_dir}//{str(idx).rjust(6, '0')}.jpg"
            cv2.imwrite(box_dir, marked_box)
            if random.random() < change_mark_chance:
                self.set_random_mark_generator()

            idx += 1
            yield box_dir, label

    def create_marked_box(self):
        box = random.choice(self._raw_answer_boxes)
        mark_functions = [(self._mark_generator.generate_mark, 1),              # - Mark
                          (self._mark_generator.generate_unmark, 0),            # - Unmark
                          (lambda: np.zeros(self._shape, dtype=np.uint8), 0)]   # - Empty box

        mark_func, label = random.choice(mark_functions)
        marked_box = cv2.subtract(box, mark_func())
        marked_box[marked_box < 0] = 0
        return marked_box, label

    def extract_boxes(self):
        answer_boxes = self._extract_boxes(self.ANSWER_BOXES_PATH, 4, 10)
        index_image = self._extract_boxes(self.INDEX_BOXES_PATH, 6, 10)
        return answer_boxes + index_image

    def increment_array_elements(self, arr):
        for i in range(len(arr)):
            arr[i] += 9 * i
        return arr

    def _extract_boxes(self, path: str, x: int, y: int):
        boxes = []
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        x_parts = np.linspace(0., img.shape[1] - 2 * self._border_x - ((math.ceil(img.shape[1] / 90)) - 1) * 9, x + 1) + self._border_x - 3
        y_parts = np.linspace(0., img.shape[0] - 2 * self._border_y - ((math.ceil(img.shape[0] / 90)) - 1) * 9, y + 1) + self._border_y - 3
        y_parts = self.increment_array_elements(y_parts)
        x_parts = self.increment_array_elements(x_parts)
        for y0, y1 in zip(y_parts[:-1], y_parts[1:]):
            for x0, x1 in zip(x_parts[:-1], x_parts[1:]):
                box = img[int(y0) - self._box_offset: int(y1) + self._box_offset,
                          int(x0) - self._box_offset: int(x1) + self._box_offset]
                boxes.append(cv2.resize(box, dsize=self._shape))
        return boxes


if __name__ == '__main__':
    TrainingDataGenerator(box_offset=3).generate(100000)
