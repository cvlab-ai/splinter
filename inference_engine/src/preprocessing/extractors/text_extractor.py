from .extractor import Extractor


class TextExtractor(Extractor):
    def process(self, *args, **kwargs):
        self.remove_borders(7)
        self.detect_and_remove_lines()
        return self._operated_img
