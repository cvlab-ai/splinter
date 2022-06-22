import random

import cv2
import numpy as np
from matplotlib import pyplot as plt

from research.mark_generator import MarkGenerator, Mark
from research.exam_solver import ExamSolver


class MarkedAnswerCardGenerator:
    MARK_CHANCE = 0.4
    UNMARK_CHANCE = 0.1

    def __init__(self, image_path: str):
        self.exam_solver = ExamSolver(image_path)
        self.mark_generator = self.create_random_mark_generator()

    def create_random_mark_generator(self):
        shape = self.exam_solver.box_shape
        return MarkGenerator(shape, Mark.CROSS, Mark.CIRCLE, 0.1, 0.1, 0.1, 0.1)

    def generate(self):
        answer_card = self.exam_solver.get_answer_card()
        positions = self.exam_solver.box_positions
        positions_len = len(positions)
        for i, position in enumerate(positions):
            draw = random.random()
            if draw < MarkedAnswerCardGenerator.UNMARK_CHANCE:
                mark_mask = self.mark_generator.generate_unmark()
            elif draw < MarkedAnswerCardGenerator.MARK_CHANCE:
                mark_mask = self.mark_generator.generate_mark()
            else:
                continue
            position = position[0]
            position -= (np.array(mark_mask.shape) / 2).astype("int32")
            mark_mask = cv2.cvtColor(mark_mask, cv2.COLOR_GRAY2BGR)
            if 0 < position[1] < answer_card.shape[0] - mark_mask.shape[0] and \
                    0 < position[0] < answer_card.shape[1] - mark_mask.shape[1]:
                answer_card[position[1]:position[1] + mark_mask.shape[1], position[0]:position[0] + mark_mask.shape[0]] -= mark_mask
            print(f"\rGenerate {i}/{positions_len} mark", end="")
        print()

        plt.imshow(answer_card)
        plt.show()


if __name__ == "__main__":
    marked_answer_card_generator = MarkedAnswerCardGenerator("research/data/exams/image--000.jpg")
    marked_answer_card_generator.generate()
