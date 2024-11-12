import cv2
import numpy as np


class ImageProcessor:
    """A utility class for image processing tasks"""

    @staticmethod
    def to_grayscale(image: np.ndarray) -> np.ndarray:
        """Converts an image to grayscale.

        Args:
            image (np.ndarray): The input image.

        Returns:
            np.ndarray: Grayscale image.
        """
        if len(image.shape) > 2:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        return image

    @staticmethod
    def to_binary(image: np.ndarray, adaptive: bool = True, threshold: int = 127) -> np.ndarray:
        """Converts an image to binary (black and white) format.

        Args:
            image (np.ndarray): The input grayscale image.
            adaptive (bool): If True, uses adaptive thresholding. If False, uses simple thresholding.
            threshold (int): Threshold value for simple thresholding.

        Returns:
            np.ndarray: Binary image.
        """
        if adaptive:
            return cv2.adaptiveThreshold(
                image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 5
            )

        _, binary_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
        return binary_image

    @staticmethod
    def remove_noise(image: np.ndarray, kernel_size: tuple = (3, 3)) -> np.ndarray:
        """Applies morphological opening and denoising to remove small noise.

        Args:
            image (np.ndarray): The binary image.
            kernel_size (tuple): Size of the kernel for morphological opening.

        Returns:
            np.ndarray: Denoised image.
        """
        cleaned = cv2.morphologyEx(image, cv2.MORPH_OPEN, np.ones(kernel_size, np.uint8))
        return cv2.fastNlMeansDenoising(cleaned, h=30)

    @staticmethod
    def crop_image(image: np.ndarray, coordinates: tuple[int, int, int, int]) -> np.ndarray:
        """Crops an image to the specified coordinates.

        Args:
            image (np.ndarray): The input image.
            coordinates (tuple[int, int, int, int]): The coordinates (x, y, width, height) to crop the image.

        Returns: np.ndarray: The cropped image.
        """
        x, y, w, h = coordinates
        cropped_image = image[y:y + h, x:x + w]
        return cropped_image
