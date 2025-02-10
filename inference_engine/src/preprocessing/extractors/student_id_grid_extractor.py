from src.preprocessing import Field
from src.utils import ImageGridDivider
from .extractor import Extractor
from src.config import Config


class StudentIdGridExtractor(Extractor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_grid_divider = ImageGridDivider(
            rows=10,
            cols=6,
            group_by='x',
            target_size=Config.inference.target_box_shape,
        )

    def process(self):
        divided_image = self.image_grid_divider.divide(self._operated_img)
        return Field(divided_image, self._rect)
