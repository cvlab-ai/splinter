import json
import typing as tp

from pydantic import validator

from .extended_base_model import ExtendedBaseModel


class ResultsDTO(ExtendedBaseModel):
    exam_title: str
    student_name: str
    date: str
    exam_key: tp.List[int]
    student_id: str
    answers: tp.Dict[int, tp.List[int]]

    @validator("exam_key", pre=True, always=True)
    def exam_key_to_list(cls, v):
        return [int(answer) for answer in v[0]]

    @validator("answers", pre=True, always=True)
    def answers_to_list(cls, v):
        return {i + 1: [int(answer) for answer in row] for i, row in enumerate(v)}

    def __str__(self):
        output = []
        for field, result in self.dict().items():
            if isinstance(result, tp.Dict):
                answers_output = {}
                for k, answer in result.items():
                    if 1 in answer:
                        answers_output[k] = ", ".join(
                            [
                                chr(ord("A") + idx)
                                for idx, val in enumerate(answer)
                                if val
                            ]
                        )
                output.append(f"{field}: {json.dumps(answers_output,indent=4)}")
            else:
                output.append(f"{field}: {result}")
        return "\n".join(output)
