from pydantic_yaml import YamlModel
from .exam_storage_config import ExamStorageConfig
from .paths_config import PathsConfig

DEFAULT_CONFIG_FILEPATH = "config.yaml"


class _Config(YamlModel):
    exam_storage: ExamStorageConfig = ExamStorageConfig()
    paths: PathsConfig = PathsConfig()


Config = _Config.parse_file(DEFAULT_CONFIG_FILEPATH)
