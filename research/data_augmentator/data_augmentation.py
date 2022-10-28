import random
import typing as tp

import cv2
import numpy as np


class DataAugmentator:
    def __init__(self, img: np.ndarray):
        self.__img = img
        self.augmented = img.copy()

    def get(self):
        return self.augmented

    def gaussian_noise(self, mean=0, sigma=0.1):
        noise = np.random.normal(mean, sigma, self.augmented.shape[:2])
        noise = (noise * 255).astype(np.int32)
        _augmented_int32 = noise + self.augmented
        mask_overflow_upper = self.augmented + noise >= 255
        mask_overflow_lower = self.augmented + noise < 0
        _augmented_int32[mask_overflow_upper] = 255
        _augmented_int32[mask_overflow_lower] = 0
        self.augmented = _augmented_int32.astype(np.uint8)
        return self
    
    def distort(self, orientation='horizontal', func=np.sin, x_scale=0.05, y_scale=5):
        assert orientation[:3] in ['hor', 'ver'], "dist_orient should be 'horizontal'|'vertical'"
        assert func in [np.sin, np.cos], "supported functions are np.sin and np.cos"
        assert 0.00 <= x_scale <= 0.1, "x_scale should be in [0.0, 0.1]"
        assert 0 <= y_scale <= min(self.augmented.shape[0], self.augmented.shape[1]), "y_scale should be less then image size"

        def shift(x):
            return int(y_scale * func(np.pi * x * x_scale))

        for i in range(self.augmented.shape[orientation.startswith('ver')]):
            if orientation.startswith('ver'):
                self.augmented[:, i] = np.roll(self.augmented[:, i], shift(i))
            else:
                self.augmented[i, :] = np.roll(self.augmented[i, :], shift(i))
        return self

    def shift(self, length: int = 5):
        x_shift = random.randint(-length, length)
        y_shift = random.randint(-length, length)
        img = np.roll(self.augmented, y_shift, axis=0)
        img = np.roll(img, x_shift, axis=1)
        if y_shift > 0:
            img = img[y_shift:, :]
        elif y_shift < 0:
            img = img[:y_shift, :]
        if x_shift > 0:
            img = img[:, x_shift:]
        elif x_shift < 0:
            img = img[:, :x_shift]

        self.augmented = cv2.resize(img, dsize=self.__img.shape)
        return self

