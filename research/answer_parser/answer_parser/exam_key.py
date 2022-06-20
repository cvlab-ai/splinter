import os
from io import TextIOWrapper
import re
from typing import List
from answer_parser import ANSWER_INTERNAL_DIR, logger
from answer_parser.answer import Answer


class ExamKey:
    def __init__(self, answers: List[Answer]):
        self.answers = answers

    @classmethod
    def from_file(cls, answer_file: TextIOWrapper):
        # sikp first and second line
        answer_file.readline()
        answer_file.readline()
        r = re.compile("mark|no mark|negation")
        answers = []
        for line in answer_file:
            marks = r.findall(line)
            answers.append(Answer(marks))
        return cls(answers)

    @classmethod
    def load_exam_keys(cls, source_dir: str):
        answer_dir = source_dir + "/" + ANSWER_INTERNAL_DIR
        exam_keys = []
        for file in os.listdir(answer_dir):
            if file.endswith(".txt"):
                logger.debug("Loading exam key from %s", file)
                with open(os.path.join(answer_dir, file), "r") as f:
                    exam_keys.append(cls.from_file(f))
        return exam_keys
