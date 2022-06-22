import os
from io import TextIOWrapper
import re
from typing import List
import csv
from answer_parser import ANSWER_INTERNAL_DIR, logger
from answer_parser.answer import Answer


class ExamKey:
    def __init__(self, name: str, answers: List[Answer]):
        self.name = name
        self.answers = answers

    def to_csv(self, dest_dir: str):
        # output_dir = os.path.join(dest_dir,output_subdir)
        # if os.path.isdir(output_dir) and os.listdir(path=output_dir):
        #     logger.warn("")
        # os.mkdir(path)
        with open(
            os.path.join(dest_dir, os.path.splitext(self.name)[0] + ".csv"),
            "w",
            newline="",
        ) as csv_file:
            exam_writer = csv.writer(
                csv_file
            )
            for answer in self.answers:
                exam_writer.writerow(answer.to_ground_truth())

    @classmethod
    def from_file(cls, answer_filepath: str):
        with open(answer_filepath, "r") as answer_file:
            # sikp first and second line
            answer_file.readline()
            answer_file.readline()
            r = re.compile("mark|no mark|negation")
            answers = []
            for line in answer_file:
                marks = r.findall(line)
                answers.append(Answer(marks))
        return cls(os.path.basename(answer_filepath), answers)

    @classmethod
    def load_exam_keys(cls, source_dir: str):
        answer_dir = source_dir + "/" + ANSWER_INTERNAL_DIR
        exam_keys = []
        for file in os.listdir(answer_dir):
            if file.endswith(".txt"):
                logger.debug("Loading exam key from %s", file)
                exam_keys.append(cls.from_file(os.path.join(answer_dir, file)))
        return exam_keys
