import cv2
import numpy as np

from src.preprocessing import Field
from .extractor import Extractor


class TextExtractor(Extractor):
    """Extracts text-based fields by converting the image to black and white and removing noise."""

    def process(self) -> Field:
        """Processes the image by converting it to black and white and removing noise.

        Returns:
            Field: A Field object containing the processed image with text.
        """
        processed_image = self._prepare_text_image(self._operated_img)
        return Field(processed_image, self._rect)

    @staticmethod
    def _prepare_text_image(image: np.ndarray) -> np.ndarray:
        """Converts an image to black and white with noise reduction for better text clarity.

        This method performs the following steps:
            - Converts the image to grayscale.
            - Applies adaptive thresholding to convert to black and white.
            - Uses morphological opening to remove small noise.
            - Applies non-local means denoising to reduce remaining noise.

        Args:
            image (np.ndarray): The input image to be processed.

        Returns:
            np.ndarray: The processed black-and-white image with reduced noise.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        bw = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 5
        )
        cleaned = cv2.morphologyEx(bw, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        return cv2.fastNlMeansDenoising(cleaned, h=30)
