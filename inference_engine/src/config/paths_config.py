from pydantic import BaseModel


class PathsConfig(BaseModel):
    answer_model_path: str = "data/model/saved_model.xml",
    index_model_path: str = "data/model/handwritten-english-recognition-0001.xml"
