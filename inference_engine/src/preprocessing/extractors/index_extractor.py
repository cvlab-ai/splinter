from .extractor import Extractor


class IndexExtractor(Extractor):

    def process(self):
        self.remove_borders(15).to_binary(10)
        rectangles = self.detect_rectangles()
        rectangles_by_area = sorted(rectangles, key=lambda x: x[2] * x[3])
        rectangle_images = [self._operated_img[y:y + h, x:x + w] for x, y, w, h in rectangles_by_area]
        index_number_field, index_answer_field = rectangle_images

        # Process the index as a numeric field
        index_field_extractor = Extractor(index_number_field)
        index_field_extractor.remove_borders(5)
        index_field_extractor.detect_and_remove_lines()
        index_field_extractor.recover()
        return index_field_extractor.process()
