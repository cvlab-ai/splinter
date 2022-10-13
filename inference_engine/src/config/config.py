from pydantic_yaml import YamlModel
from .exam_storage_config import ExamStorageConfig
from .paths_config import PathsConfig
from .inference_config import InferenceConfig
from .exam_config import ExamConfig

DEFAULT_CONFIG_FILEPATH = "config.yaml"


class _Config(YamlModel):
    exam: ExamConfig = ExamConfig()
    exam_storage: ExamStorageConfig = ExamStorageConfig()
    paths: PathsConfig = PathsConfig()
    inference: InferenceConfig = InferenceConfig()


Config = _Config.parse_file(DEFAULT_CONFIG_FILEPATH)
