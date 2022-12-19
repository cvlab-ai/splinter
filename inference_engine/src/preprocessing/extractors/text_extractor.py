from .extractor import Extractor
from .field_extractor import Field


class TextExtractor(Extractor):
    def process(self, *args, **kwargs):
        self.remove_borders(7)
        self.detect_and_remove_lines()
        return super(TextExtractor, self).process()
