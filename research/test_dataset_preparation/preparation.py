import typing as tp
from random import choice

import numpy as np
import cv2
import os

from matplotlib import pyplot as plt
from matplotlib import collections as mc

from matplotlib.patches import Rectangle
import matplotlib.colors as mcolors


def show_img(img: np.ndarray):
    plt.imshow(img)
    plt.show()


def vis(img, rectangles: tp.List[tp.List[int]] = None, lines: tp.List[tp.List[int]] = None, title: str = ""):
    rectangles = rectangles or []
    lines = lines or []

    fig, ax = plt.subplots()
    # if len(img.shape) > 2:
    #     img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    ax.imshow(img)
    for (x1, y1, w1, h1) in rectangles:
        color = choice(list(mcolors.CSS4_COLORS.keys()))
        rect = Rectangle((x1, y1), w1, h1, linewidth=2, edgecolor=color, facecolor='none')
        ax.add_patch(rect)

    lc = mc.LineCollection(lines, linewidths=2)
    ax.add_collection(lc)
    plt.title(title)
    plt.show()


def load_images(dir: str):
    img_filenames = os.listdir(dir)
    images = {filename[:-4]: cv2.imread(os.path.join(dir, filename), cv2.IMREAD_COLOR) for filename in img_filenames}
    return images


def load_labels(dir: str):
    labels_dir = os.listdir(dir)
    return {filename[:-4]: [int(x) for x in str(open(os.path.join(dir, filename), 'r+').readline(4))] for filename in labels_dir if filename[-7:-4] != "(1)"}


def extract_boxes(img: np.ndarray) -> tp.List[np.ndarray]:

    vertical = detect_lines(img, (1, 16))
    print(vertical)
    show_img(img)


def to_grayscale(img) -> np.ndarray:
    if len(img.shape) > 2:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def to_binary(img, threshold: int = 220) -> np.ndarray:
    img[img <= threshold] = 0
    img[img > threshold] = 255
    return img


def erode(img, kernel: tp.Tuple[int, int] = None) -> np.ndarray:
    if kernel is None:
        kernel = (4, 4)
    kernel = np.ones(kernel, np.uint8)
    img = cv2.erode(img, kernel)
    return img


def detect_lines(img: np.ndarray, kernel_size: tp.Tuple[int, int]):
    negative = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    detect = cv2.morphologyEx(negative, cv2.MORPH_OPEN, kernel, iterations=2)
    contours = cv2.findContours(detect, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours: np.ndarray = contours[0] if len(contours) == 2 else contours[1]
    lines = []
    for contour in contours:
        contour = contour.reshape((contour.shape[0], 2))
        if kernel_size[0] > kernel_size[1]:  # Detect horizontal lines
            y_mean = int(contour.mean(axis=0)[1])
            lines.append(
                np.array(
                    [[contour.min(axis=0)[0], y_mean], [contour.max(axis=0)[0], y_mean]]
                )
            )
        else:  # Detect vertical lines
            x_mean = int(contour.mean(axis=0)[0])
            lines.append(
                np.array(
                    [[x_mean, contour.min(axis=0)[1]], [x_mean, contour.max(axis=0)[1]]]
                )
            )
    return lines


if __name__ == '__main__':
    images = load_images('data/poprawiony_dataset/answerDataset/images')
    labels = load_labels('data/poprawiony_dataset/answerDataset/labels')
    connected = {}
    for filename, image in list(images.items()):
        connected[filename] = (labels[filename], image)

    foo = []
    for filename, (label, image) in list(connected.items()):
        proc_images = erode(to_binary(to_grayscale(image)))
        vertical_lines = detect_lines(proc_images, (1, 20))
        horizontal_lines = detect_lines(proc_images, (20, 1))
        if len(vertical_lines) < 6:
            continue

        x0 = min(line[0][0] for line in vertical_lines)
        x1 = max(line[0][0] for line in vertical_lines)

        if x1 - x0 < 200:
            continue
        operated_lines = list(sorted(vertical_lines, key=lambda line: abs(line[1][1] - line[0][1]), reverse=True))

        try:
            operated_line = next(x for x in operated_lines if 40 < abs(x[1][1] - x[0][1]) <= 50)
        except StopIteration:
            continue

        y0 = int(min(operated_line[1][1], operated_line[0][1]))
        y1 = int(max(operated_line[1][1], operated_line[0][1]))
        foo.append(y1 - y0)
        proc_images = proc_images[y0:y1, x0:x1]
        result = image[y0:y1, x0:x1]
        x_values = np.linspace(0, result.shape[1], 5, dtype=int)

        for idx, ((x0, x1), l) in enumerate(zip(zip(x_values[:-1], x_values[1:]), label)):
            box = result[:, x0:x1]
            output_dir = f'{os.path.dirname(__file__)}/sep_boxes/{l}'
            cv2.imwrite(os.path.join(output_dir, filename + str(idx) + '.jpg'), box)

    print(len(np.array(foo)))
    print(min(np.array(foo)))
