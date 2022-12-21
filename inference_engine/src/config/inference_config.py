from pydantic import BaseModel


class InferenceConfig(BaseModel):
    answer_threshold: float = 0.5
    answer_row_shape: tuple = (290, 60)
    debug_image: bool = False
