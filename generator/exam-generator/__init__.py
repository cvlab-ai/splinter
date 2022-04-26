from .logger import Logger
from .generator_config import GeneratorConfig
from .exam_generator import ExamGenerator
from .instruction_generator import generate_exam_instruction

# TODO
# [ ] Random fonts + add config
# [ ] Random margins + add config
# [ ] Random interlines between questions + add config
# [ ] Generate identifier for an exam - to identify it after gathering from participants (maybe in footer)
# [ ] Generate and save metadata for every generated exam
# [ ] Export config to json
# [ ] Add zipify to exams (make bundles)