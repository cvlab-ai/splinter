from .extractor import Extractor


class GroupExtractor(Extractor):
    def process(self, *args, **kwargs):
        self.remove_borders(5)
        return self.split_image_into_squares(4, 1, group_by='y')
