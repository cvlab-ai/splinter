from src.preprocessing import Field
from .extractor import Extractor
from .text_extractor import TextExtractor

class StudentIdTextExtractor(Extractor):

    def process(self):
        return TextExtractor(Field(self._operated_img, self._rect)).process()
