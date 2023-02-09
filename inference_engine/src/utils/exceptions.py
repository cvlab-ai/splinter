
class ExamInvalid(Exception):
    DIRNAME = None


class ExamNotDetected(ExamInvalid):
    DIRNAME = "unknown"


class IndexNotDetected(ExamInvalid):
    DIRNAME = "no_index"


class PreprocessingError(ExamInvalid):
    DIRNAME = "error"
