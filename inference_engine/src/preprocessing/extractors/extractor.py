import numpy as np

from src.preprocessing import Field


class Extractor:

    def __init__(self, field: Field):
        self._rect = field.rect
        self._operated_img: np.ndarray = field.img.copy()
        self._original_img: np.ndarray = field.img
