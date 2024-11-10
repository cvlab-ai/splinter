from src.preprocessing import Field
from .extractor import Extractor
from .image_grid_divider import ImageGridDivider


class GroupExtractor(Extractor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_grid_divider = ImageGridDivider(
            rows=1,
            cols=4,
            target_size=(90, 90),
            group_by='y'
        )

    def process(self):
        groups = self.image_grid_divider.divide(self._operated_img)
        return Field(groups, self._rect)
