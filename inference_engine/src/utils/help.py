import cv2

import matplotlib
import numpy as np

matplotlib.use('TkAgg')
from matplotlib import pyplot as plt


def show_image(img: np.ndarray, title: str = ""):
    if len(img.shape) != 3:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    plt.title(title)
    plt.imshow(img)
    plt.show()
