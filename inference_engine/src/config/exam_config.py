from pydantic import BaseModel


class ExamConfig(BaseModel):
    number_of_columns: int = 5
