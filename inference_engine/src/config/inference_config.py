from pydantic import BaseModel


class InferenceConfig(BaseModel):
    answer_threshold: float = 0.5
