import cv2
import numpy as np

from src.utils.exceptions import ExamNotDetected


def constrast_exam(image: np.ndarray):
    try:
        # return cv2.convertScaleAbs(image, alpha=1.5, beta=0.0)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        clahe_image = clahe.apply(gray_image)

        clahe_image = cv2.cvtColor(clahe_image, cv2.COLOR_GRAY2BGR)

        _, thresholded_image = cv2.threshold(clahe_image, 200, 255, cv2.THRESH_BINARY_INV)
        clahe_image = thresholded_image
        clahe_image = cv2.bitwise_not(clahe_image)

        return clahe_image
    except Exception as e:
        raise ExamNotDetected(e)
