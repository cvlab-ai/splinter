import logging

import numpy as np
import cv2
import re

from .model import Model


class OCRModel(Model):
    letters = '~ !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_abcdefghijklmnopqrstuvwxyz{|}~£'

    def inference(self, _input: np.array, only_digits: bool = False,  *args, **kwargs):
        try:
            h, w = _input.shape
            i_b, i_c, i_h, i_w = self.input_layer.partial_shape
            i_h, i_w = i_h.get_length(), i_w.get_length()
            ratio = i_h / h
            _input = cv2.resize(_input, (int(ratio * w), i_h), interpolation=cv2.INTER_AREA)[None]
            _input = np.pad(_input, ((0, 0), (0, 0), (0, i_w - int(ratio * w))), mode='edge')[None]
            return super(OCRModel, self).inference(_input, only_digits)
        except (ValueError, IndexError):
            logging.error("Cannot read index properly")
            return ""

    def _decode(self, predictions, only_digits: bool = False, *args, **kwargs):
        # Select max probability (greedy decoding) then decode index to character
        preds_index = np.argmax(predictions, 2)  # WBD - > WB
        preds_index = preds_index.transpose(1, 0)  # WB -> BW
        preds_index_reshape = preds_index.reshape(-1)  # B*W

        char_list = []
        odds_list = []
        for i in range(len(preds_index_reshape)):
            if preds_index_reshape[i] != 0 and (not (i > 0 and preds_index_reshape[i - 1] == preds_index_reshape[i])):
                char_list.append(self.letters[preds_index_reshape[i]])
                odds_list.append(max(predictions[preds_index_reshape[i]][0]))
        text = ''.join(char_list)
        return re.sub("[^0-9]", "", text) if only_digits else text # Remove all non-numeric characters
