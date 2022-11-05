import numpy as np

from .model import Model
from src.config import Config


class BoxIndexModel(Model):
    def inference(self, _input: np.array, *args, **kwargs):
        return [np.argmax(self.model([column])[0]) for column in _input]

    def _decode(self, predictions: np.ndarray):
        pass
