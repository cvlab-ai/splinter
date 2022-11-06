import numpy as np

from .model import Model
from src.config import Config
from src.utils import show_image


class BoxModel(Model):
    def inference(self, _input: np.array, argmax: bool = False, *args, **kwargs):
        if argmax:
            return [np.argmax(self.model([vals])[self.output_layer]) for vals in _input]
        else:
            return [(self.model([vals])[self.output_layer] > Config.inference.answer_threshold).astype(int)
                    for vals in _input]
