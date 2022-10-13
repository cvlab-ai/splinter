from .extractors import TextExtractor, IndexExtractor, RowsExtractor, FieldExtractor
from .help import *
from .fields import Fields


class Preprocessing:
    FIELD_EXTRACTOR_MAPPING = {
        Fields.exam_title: TextExtractor,
        Fields.student_name: TextExtractor,
        Fields.student_group: TextExtractor,
        Fields.date: TextExtractor,
        Fields.student_id: IndexExtractor,
        Fields.answers_rows: RowsExtractor
    }

    def __init__(self, img: np.ndarray):
        self._exam_copy = img.copy()

    def process(self) -> tp.Dict[Fields, np.ndarray]:
        fields = FieldExtractor(self._exam_copy).process()
        _map = Preprocessing.FIELD_EXTRACTOR_MAPPING
        result = {f: _map[f](img).process() for f, img in fields.items() if f in _map}
        return result
