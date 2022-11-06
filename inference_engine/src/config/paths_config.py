from pydantic import BaseModel


class PathsConfig(BaseModel):
    box_model_path: str = "data/model/saved_model.xml",
    ocr_model_path: str = "data/model/handwritten-english-recognition-0001.xml"
