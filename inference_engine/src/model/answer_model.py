import numpy as np

from .model import Model
from src.config import Config


class AnswerModel(Model):
    def _decode(self, predictions: np.ndarray):
        return (predictions > Config.inference.answer_threshold).astype(int)
