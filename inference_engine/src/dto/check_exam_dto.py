from .extended_base_model import ExtendedBaseModel


class CheckExamDTO(ExtendedBaseModel):
    exam_path: str
    exam_name: str
