from .extractor import Extractor


class RowsExtractor(Extractor):
    def process(self):
        self.remove_borders(10)
        horizontal = self.detect_lines((256, 1))
        y_values = sorted([p1[1] for p1, p2 in horizontal])
        y_values = self.fill_missing_values(y_values, self._operated_img.shape[0], 15)
        y_values = self.ensure_correct_distribution(y_values)
        return [self._operated_img[y1:y2, :] for y1, y2 in zip(y_values[:-1], y_values[1:])]
