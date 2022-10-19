from .extractor import Extractor


class GroupExtractor(Extractor):
    def process(self, *args, **kwargs):
        self.remove_borders(5)
        return self._operated_img
