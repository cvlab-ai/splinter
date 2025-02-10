import numpy as np
from ultralytics import YOLO

from src.config import Config


class BoxModelYolo:

    def __init__(self, model_path: str):
        self.model = YOLO(model_path, verbose=False)

    def inference(self, _input: np.array, argmax: bool = False, *args, **kwargs):
        results = [
            np.array([self.model(image, verbose=False)[0].probs.data[1].item() for image in part]).reshape(-1, 1)
            for part in _input
        ]

        if argmax:
            return np.argmax(results, axis=1).flatten(), np.max(results, axis=1).flatten()

        return [(result > Config.inference.answer_threshold).astype(int) for result in results]
