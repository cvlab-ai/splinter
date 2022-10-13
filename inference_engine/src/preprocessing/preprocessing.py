from .extractors import IndexExtractor, RowsExtractor, FieldExtractor
from .help import *
from .fields import Fields


class Preprocessing:
    FIELD_EXTRACTOR_MAPPING = {
        Fields.student_id: IndexExtractor,
        Fields.answers_rows: RowsExtractor
    }

    def __init__(self, img: np.ndarray):
        self._exam_copy = img.copy()

    def process(self) -> tp.Dict[Fields, np.ndarray]:
        fields = FieldExtractor(self._exam_copy).process()
        _map = Preprocessing.FIELD_EXTRACTOR_MAPPING
        return {f: _map[f](img).process() for f, img in fields.items() if f in _map}
