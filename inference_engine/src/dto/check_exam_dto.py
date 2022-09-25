from dataclasses import dataclass
from dataclass_wizard import JSONWizard


@dataclass
class CheckExamDTO(JSONWizard):
    exam_path: str
    exam_name: str
