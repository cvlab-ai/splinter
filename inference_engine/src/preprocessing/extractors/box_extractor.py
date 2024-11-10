from src.preprocessing import Field
from src.utils import ImageGridDivider
from .extractor import Extractor


class BoxExtractor(Extractor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_grid_divider = ImageGridDivider(
            rows=10,
            cols=4,
            target_size=(90, 90),
            group_by='y'
        )

    def process(self):
        divided_image = self.image_grid_divider.divide(self._operated_img)
        return Field(divided_image, self._rect)
