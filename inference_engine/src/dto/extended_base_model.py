from pydantic import BaseModel
from humps import camel


def to_camel(_str: str) -> str:
    return camel.case(_str)


class ExtendedBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel
