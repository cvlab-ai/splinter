from .extended_base_model import ExtendedBaseModel


class CheckPdfDTO(ExtendedBaseModel):
    exam_id: int
    file_name: str
    force: bool = False
