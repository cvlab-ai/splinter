from .extractor import Extractor
from src.preprocessing import Field


class IndexExtractor(Extractor):
    def process(self):
        horizontal = self.detect_lines((64, 1))
        y_values = sorted([p1[1] for p1, p2 in horizontal])
        self.fill_missing_values(y_values, self._operated_img.shape[0], 15)
        index_text, index_answer = self._operated_img[:y_values[1], :], self._operated_img[y_values[1]:, :]
        text_rect = (self._rect[0], self._rect[1], *index_text.shape[::-1])
        index_text_extractor = Extractor(Field(index_text, text_rect))
        index_text_extractor.remove_borders(2)
        index_text_extractor.detect_and_remove_lines()
        index_text_extractor.recover()
        answer_rect = (self._rect[0], self._rect[1] + y_values[1], *index_answer.shape[::-1])
        index_answer_extractor = Extractor(Field(index_answer, answer_rect))
        boxes_field = Field(index_answer_extractor.split_image_into_squares(6, 10, group_by='x'), answer_rect)
        return boxes_field, index_text_extractor.process()
