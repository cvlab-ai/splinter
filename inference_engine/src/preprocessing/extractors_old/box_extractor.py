from .extractor import Extractor
from src.preprocessing import Field


class BoxExtractor(Extractor):
    def process(self):
        self.remove_borders(3)
        images = self.split_image_into_squares(4, 10, group_by='y')
        return Field(images, self._rect)
