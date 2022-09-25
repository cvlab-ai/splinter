from dataclasses import dataclass
from dataclass_wizard import JSONWizard


@dataclass
class CheckExamsDTO(JSONWizard):
    exam_path: str
