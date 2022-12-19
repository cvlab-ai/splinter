
class ExamInvalid(Exception):
    FILENAME = None


class ExamNotDetected(ExamInvalid):
    FILENAME = "unknown"


class IndexNotDetected(ExamInvalid):
    FILENAME = "no_index"


class PreprocessingError(ExamInvalid):
    FILENAME = "no_index"
