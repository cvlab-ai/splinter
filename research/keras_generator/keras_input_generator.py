import typing as tp

import numpy as np
import keras

from research.marked_answer_card_generator import MarkedAnswerCardGenerator


class KerasDataGenerator(keras.utils.Sequence):
    def __init__(
        self,
        card_generator: MarkedAnswerCardGenerator,
        dim: tuple = (260, 90),
        n_channels: int = 1,
        n_answers: int = 4,
        batch_size: int = 40,
        data_in_epoch: int = 200,
    ):
        self.dim = dim
        self.batch_size = batch_size
        self.row_generator: tp.Generator[
            tp.Tuple[np.ndarray, np.ndarray[np.int]]
        ] = card_generator.row_generator()
        self.data_in_epoch = data_in_epoch
        assert (
            self.data_in_epoch and not self.data_in_epoch % self.batch_size
        ), f"Elements in epoch are not dividable by batch size!"
        self.n_channels = n_channels
        self.n_answers = n_answers

    def __len__(self):
        return int(np.floor(self.data_in_epoch / self.batch_size))

    def __getitem__(self, _):
        X, y = self.data_generation()
        return X, y

    def data_generation(self):
        X = np.empty((self.batch_size, *self.dim, self.n_channels), dtype=np.float)
        y = np.empty((self.batch_size, self.n_answers), dtype=np.int)
        for batch_idx in range(self.batch_size):
            (
                X[
                    batch_idx,
                ],
                y[
                    batch_idx,
                ],
            ) = next(self.row_generator)
        return X, y
