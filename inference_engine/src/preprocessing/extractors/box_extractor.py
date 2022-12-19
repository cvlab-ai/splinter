from .extractor import Extractor


class BoxExtractor(Extractor):
    def process(self):
        self.remove_borders(3)
        return self.split_image_into_squares(4, 10, group_by='y')
