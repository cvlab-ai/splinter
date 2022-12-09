from .extractor import Extractor


class BoxExtractor(Extractor):
    def process(self):
        self.remove_borders(3)
        self.brighten_up(0.7)
        return self.split_image_into_squares(4, 10, group_by='y')
