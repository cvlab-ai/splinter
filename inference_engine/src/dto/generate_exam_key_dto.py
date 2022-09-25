from dataclasses import dataclass
from dataclass_wizard import JSONWizard


@dataclass
class GenerateExamKeyDTO(JSONWizard):
    exam_path: str
