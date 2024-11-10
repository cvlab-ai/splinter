from src.preprocessing import Field
from src.utils import ImageProcessor
from .extractor import Extractor


class TextExtractor(Extractor):
    """Extracts text-based fields by converting the image to black and white and removing noise."""

    def process(self) -> Field:
        """Processes the image by converting it to black and white and removing noise.

        Returns:
            Field: A Field object containing the processed image with text.
        """
        gray = ImageProcessor.to_grayscale(self._operated_img)
        binary = ImageProcessor.to_binary(gray, adaptive=True)
        cleaned = ImageProcessor.remove_noise(binary)
        return Field(cleaned, self._rect)
