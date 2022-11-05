from .extractor import Extractor


class RowsExtractor(Extractor):
    def process(self):
        self.remove_borders(10)
        return self.split_image_into_squares(4, 10)
