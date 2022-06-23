from enum import Enum
from typing import List


class Mark(Enum):
    NO_MARK = 1
    MARK = 2
    NEGATION = 3


class Answer:

    gt_map = {Mark.NO_MARK: "0", Mark.MARK: "1", Mark.NEGATION: "2"}

    def __init__(self, marks: List[str]):
        self.marks = []
        for mark in marks:
            if mark == "mark":
                self.marks.append(Mark.MARK)
            elif mark == "no mark":
                self.marks.append(Mark.NO_MARK)
            elif mark == "negation":
                self.marks.append(Mark.NEGATION)

    def to_ground_truth(self):
        gt = []
        for mark in self.marks:
            gt.append(self.gt_map[mark])
        return gt
