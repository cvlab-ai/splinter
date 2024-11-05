from .extractor import Extractor
from src.preprocessing import Field


class GroupExtractor(Extractor):
    def process(self, *args, **kwargs):
        self.remove_borders(5)
        return Field(self.split_image_into_squares(4, 1, group_by='y'), self._rect)
