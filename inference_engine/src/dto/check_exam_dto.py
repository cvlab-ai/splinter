from .extended_base_model import ExtendedBaseModel


class CheckExamDTO(ExtendedBaseModel):
    exam_id: int
    force: bool = False
