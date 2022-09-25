import typing as tp
import random
import pathlib

import cv2
import numpy as np
from matplotlib import pyplot as plt

from research.mark_generator import MarkGenerator, Mark
from research.exam_solver import ExamSolver
from research.data_augmentator import DataAugmentation


class MarkedAnswerCardGenerator:
    MARK_CHANCE = 0.4
    UNMARK_CHANCE = 0.1

    def __init__(self, image_path: str, input_shape: tp = (260, 90)):
        self._input_shape = input_shape
        self.exam_solver = ExamSolver(image_path)
        self.mark_generator = self._create_random_mark_generator()

    def _create_random_mark_generator(self):
        shape = self.exam_solver.box_shape
        shape = (shape * 0.5).astype(int)
        return MarkGenerator(shape, Mark.CROSS, Mark.CIRCLE, 0.1, 0.1, 0.2, 0.1)

    def box_generator(self, augmentation: bool = True):
        boxes_dir = self.box_dataset_dir()
        file_counter = 1
        while True:
            answer_card, labels = self.generate_filled_card()
            plt.imshow(answer_card)
            plt.show()
            if augmentation:
                data_augmentation = DataAugmentation(answer_card)
                data_augmentation.gaussian_noise()
                answer_card = data_augmentation.augmented
            for box_row, row_label in zip(self.exam_solver.box_positions, labels):
                for box_position, label in zip(box_row, row_label):
                    box_img = self.extract_box(answer_card, box_position)
                    box_dir = f"{boxes_dir}/{str(file_counter).rjust(6, '0')}.jpg"
                    cv2.imwrite(box_dir, box_img)
                    file_counter += 1
                    yield box_dir, label

    @staticmethod
    def box_dataset_dir():
        path = pathlib.Path('research/data/boxes')
        path.mkdir(parents=True, exist_ok=True)
        return str(path.absolute())

    def row_generator(self):
        while True:
            answer_card, labels = self.generate_filled_card()
            data_augmentation = DataAugmentation(answer_card)
            data_augmentation.gaussian_noise()
            for box_row, row_label in zip(self.exam_solver.box_positions, labels):
                yield self.extract_row(data_augmentation.augmented, box_row), row_label

    def generate_filled_card(self):
        answer_card = self.exam_solver.get_answer_card()
        labels = []
        for box_row in self.exam_solver.box_positions:
            row_labels = np.zeros(shape=4, dtype=np.uint8)
            for i, box_position in enumerate(box_row):
                mark_mask, label = self._get_mark()
                self._merge_mask(mark_mask, box_position, answer_card)
                row_labels[i] = label
            labels.append(row_labels)
        return answer_card, labels

    def extract_box(self, answer_card: np.ndarray, box_position: np.ndarray):
        height_correction = -12
        box_shape = self.exam_solver.box_shape + (0, height_correction)
        min_x, min_y = (box_position - box_shape / 2).astype(dtype=np.int32)
        max_x, max_y = (box_position + box_shape / 2).astype(dtype=np.int32)
        extracted = answer_card[min_y: max_y, min_x: max_x]
        resized_row = cv2.resize(extracted, dsize=self._input_shape)
        return resized_row

    def extract_row(self, answer_card: np.ndarray, box_row: np.ndarray):
        # TODO Get row position from exam solver
        height_correction = -12
        box_shape = self.exam_solver.box_shape + (0, height_correction)
        min_x, min_y = (np.min(box_row, axis=0) - box_shape / 2).astype(dtype=np.int32)
        max_x, max_y = (np.max(box_row, axis=0) + box_shape / 2).astype(dtype=np.int32)
        extracted = answer_card[min_y: max_y, min_x: max_x]
        resized_row = cv2.resize(extracted, dsize=self._input_shape)
        return resized_row

    @staticmethod
    def _merge_mask(mark: np.ndarray, pos: np.ndarray, answer_card: np.ndarray):
        if mark is None:
            return
        pos = pos.copy()
        pos -= (np.array(mark.shape) / 2).astype("int32")
        mark = cv2.cvtColor(mark, cv2.COLOR_GRAY2BGR)
        if 0 < pos[1] < answer_card.shape[0] - mark.shape[0] and 0 < pos[0] < answer_card.shape[1] - mark.shape[1]:
            answer_card[pos[1]:pos[1] + mark.shape[1], pos[0]:pos[0] + mark.shape[0]] -= mark

    def _get_mark(self):
        draw = random.random()
        if draw < MarkedAnswerCardGenerator.UNMARK_CHANCE:
            return self.mark_generator.generate_unmark(), 0
        elif draw < MarkedAnswerCardGenerator.MARK_CHANCE + MarkedAnswerCardGenerator.UNMARK_CHANCE:
            return self.mark_generator.generate_mark(), 1
        else:
            return None, 0


if __name__ == "__main__":
    marked_answer_card_generator = MarkedAnswerCardGenerator("research/data/exams/image--000.jpg", (90, 90))
    row_generator = marked_answer_card_generator.box_generator(augmentation=False)
    for i, (box_path, labels) in enumerate(row_generator):
        print(labels)
        # plt.imshow(img)
        # plt.show()
        if i == 10:
            break
