import numpy as np
import cv2

from .model import Model
from src.config import Config


class AnswerModel(Model):

    def inference(self, _input: np.array, *args, **kwargs):
        prepared_input = []
        for row in _input:
            prepared_row = cv2.resize(row, Config.inference.answer_row_shape)
            prepared_row = cv2.merge([prepared_row] * 3)
            prepared_input.append(prepared_row)
        return super(AnswerModel, self).inference(np.array(prepared_input))

    def _decode(self, predictions: np.ndarray):
        return (predictions > Config.inference.answer_threshold).astype(int)
