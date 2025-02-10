from src.preprocessing import Field
from src.utils import ImageGridDivider
from .extractor import Extractor
from ...config import Config


class GroupExtractor(Extractor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_grid_divider = ImageGridDivider(
            rows=1,
            cols=4,
            target_size=Config.inference.target_box_shape,
            group_by='y'
        )

    def process(self):
        """Processes the image by dividing it into a grid with a single row and multiple columns.

        Returns: A Field object containing the divided image and the rectangle.
        """
        divided_image = self.image_grid_divider.divide(self._operated_img)
        return Field(divided_image, self._rect)
