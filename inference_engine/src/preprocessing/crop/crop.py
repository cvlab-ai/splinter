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

        middle_points = [(x + w // 2, y + h // 2) for x, y, w, h in squares]

        min_x = min(point[0] for point in middle_points)
        max_x = max(point[0] for point in middle_points)
        min_y = min(point[1] for point in middle_points)
        max_y = max(point[1] for point in middle_points)

        image = image[min_y:max_y, min_x:max_x]

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