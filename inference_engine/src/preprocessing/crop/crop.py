import cv2
import numpy as np

from src.utils.exceptions import ExamNotDetected
from src.preprocessing.rotation import detect_reference_points


def crop_exam(image: np.ndarray):
    try:
        reference_points = detect_reference_points(image)

        squares = []
        for _, contour in reference_points:
            squares.append(cv2.boundingRect(contour))

        nearest, farest = __find_extreme_squares(squares)

        # crop image
        image = image[nearest[1]:farest[1] + farest[3], nearest[0]:farest[0] + farest[2]]

        return image
    except Exception as e:
        raise ExamNotDetected(e)


def __find_extreme_squares(squares):
    """
    Find the square closest to the top left
    and bottom right corners of the image
    """
    nearest_square = None
    farest_square = None
    min_distance = float('inf')
    max_distance = float('-inf')
    for square in squares:
        x, y, _, _ = square
        distance = x + y # L1
        if distance < min_distance:
            min_distance = distance
            nearest_square = square
        if distance > max_distance:
            max_distance = distance
            farest_square = square
    return nearest_square, farest_square