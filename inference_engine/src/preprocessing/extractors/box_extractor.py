import cv2
import numpy as np

from .extractor import Extractor
from .. import Field


class BoxExtractor(Extractor):
    PADDING_PX = 2
    TARGET_SIZE = (90, 90)

    def process(self):
        number_of_rows = 10
        number_of_options = 4
        answer_row_height = self._operated_img.shape[0] // number_of_rows
        answer_array = np.zeros((10, 4, 90, 90, 3), dtype=np.uint8)

        for i in range(number_of_rows):
            start_y = i * answer_row_height
            end_y = min((i + 1) * answer_row_height + self.PADDING_PX, self._operated_img.shape[0])
            answer_row = self._operated_img[start_y:end_y, :]
            answer_option_width = answer_row.shape[1] // number_of_options

            for j in range(number_of_options):
                start_x = j * answer_option_width
                end_x = (j + 1) * answer_option_width
                answer_option = answer_row[:, start_x:end_x]
                resized_answer_option = cv2.resize(answer_option, self.TARGET_SIZE)
                answer_array[i, j] = resized_answer_option

        return Field(answer_array, self._rect)
