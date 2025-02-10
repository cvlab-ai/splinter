import numpy as np
from deprecated import deprecated

from src.config import Config
from .model import Model


@deprecated(reason="This class is deprecated. Use BoxModelYolo instead.")
class BoxModel(Model):
    def inference(self, _input: np.array, argmax: bool = False, *args, **kwargs):
        if argmax:
            pred = [self.model([vals])[self.output_layer] for vals in _input]
            return np.argmax(pred, axis=1).flatten(), np.max(pred, axis=1).flatten()
        else:
            return [(self.model([vals])[self.output_layer] > Config.inference.answer_threshold).astype(int)
                    for vals in _input]
