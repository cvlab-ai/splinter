import keras
import keras.backend as K
import numpy as np

import matplotlib.pyplot as plt
import cv2

from research.mark_generator import MarkGenerator, Mark
from research.marked_answer_card_generator import MarkedAnswerCardGenerator


def macro_accuracy(y_true, y_pred):
    return K.min(K.cast(K.equal(y_true, K.round(y_pred)), dtype='float16'), axis=1)


def load_model():
    dependencies = {
        'macro_accuracy': macro_accuracy
    }
    return keras.models.load_model('research/data/models/models/CNN_answer_full.h5', custom_objects=dependencies)


def generate_row():
    template = 'image--002.jpg'
    generator = MarkedAnswerCardGenerator(f'research/data/exams/{template}')

    img = generator.generate()

    row_width = 290
    row_height = 60
    row_x = 600
    row_y = 1480

    img = cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
    row = img[row_y: row_y + row_height, row_x: row_x + row_width]

    plt.imshow(row)
    plt.show()


def model_test():
    model = load_model()
    mark_generator = MarkGenerator((32, 32), Mark.CROSS, Mark.CIRCLE, 0.2, 0.2, 0.2, 0.2)

    for i in range(3):
        test_mark_row = mark_generator.generate_row((60, 290), [False, True, True, False])
        converted_gray_scaled = cv2.merge([test_mark_row] * 3)
        test_input = np.array([converted_gray_scaled])
        answer = model.predict(test_input)
        answer_str = [f"{int(ans * 100)}%" for ans in answer[0]]
        plt.imshow(test_mark_row)
        plt.gray()
        plt.title("       ".join(answer_str))
        plt.show()


if __name__ == '__main__':
    generate_row()

