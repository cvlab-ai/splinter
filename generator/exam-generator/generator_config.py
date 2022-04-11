from __future__ import annotations

import random
import typing as tp
from dataclasses import dataclass, field
from enum import Enum, IntEnum, auto

from .config import *


class Font(Enum):
    MODERN = "modern"
    KPFONTS = "kpfonts"
    GFSDIDOT = "gfsdidot"
    UTOPIA = "fourier"
    VENTURIS = "venturis"
    LIBERTINE = "libertine"
    TERMES = "tgtermes"


class MarkType(IntEnum):
    CIRCLE = 0
    CROSS = auto()
    DOODLE = auto()
    UNDERSCORE = auto()
    # TODO outline whole question

    @staticmethod
    def is_valid(check_mark: MarkType, uncheck_mark: MarkType) -> bool:
        if any([check_mark == uncheck_mark,
                uncheck_mark == MarkType.UNDERSCORE,
                (check_mark, uncheck_mark) == (MarkType.DOODLE, MarkType.CROSS)]):
            return False
        return True


class RuleStructure(IntEnum):
    DESCRIPTION = 0
    INDEX = auto()
    EXAM_DURATION = auto()
    MAX_POINTS = auto()
    DATE = auto()
    MARK_DEMO = auto()


class AnswerLayout(IntEnum):
    ONE_COLUMN = 0
    # A) ANSWER
    # B) ANSWER
    # B) ANSWER
    # C) ANSWER
    # D) ANSWER

    TWO_COLUMNS = auto()
    # A) ANSWER         B) ANSWER
    # B) ANSWER         C) ANSWER
    # D) ANSWER

    ONE_ROW = auto()
    # A) ANSWER B) ANSWER C) ANSWER
    # D) ANSWER E) ANSWER


class QuestionLength(IntEnum):
    SHORT = 10
    MEDIUM = 30
    LONG = 50


class AnswerLength(IntEnum):
    SHORT = 4
    MEDIUM = 15
    LONG = 30


class AnswerToken(Enum):
    # Value are set as first elements from list of tokens
    BIG_LETTERS = "A"           # A B C
    SMALL_LETTERS = "a"         # a b c
    NUMBERS = "1"               # 1 2 3
    ROMAN_NUMBERS = "I"         # I II III
    DOTS = "•"                  # • • •
    DASH = "-"                  # - - -


class AnswerSeparator(Enum):
    DOT = "."                   # .
    CLOSE_PARENTHESIS = ")"     # )
    PIPE = "|"                  # |
    COLON = ":"                 # :
    SEMICOLON = ";"             # ;
    SPACE = " "                 # [[:space:]]
    SLASH = "/"                 # /
    BACKSLASH = "\\"            # \


@dataclass
class GeneratorConfig:
    # Document style
    font: Font = Font.TERMES
    font_size: int = 10
    top_margin: float = 1.0 # cm
    left_margin: float = 2.0 # cm

    # Rule section
    rule_structures: tp.List[RuleStructure] = field(default_factory=lambda: list(RuleStructure)) # get every member of RuleStructure as int
    rule_section_title: str = "Instrukcje"
    rule_description: str = "Example description"
    rule_exam_duration: int = 45
    rule_max_points: int = 20
    rule_exam_date: str = "2020.04.10"# Change to datetime to randomize it

    # Question sections
    number_of_questions: int = 6
    questions_length: tp.List[QuestionLength] = field(default_factory=lambda: [QuestionLength.MEDIUM] * (GeneratorConfig.number_of_questions))

    number_of_answers: tp.List[int] = field(default_factory=lambda: [4] * (GeneratorConfig.number_of_questions))
    answers_layout: tp.List[AnswerLayout] = field(default_factory=lambda: [AnswerLayout.ONE_COLUMN] * (GeneratorConfig.number_of_questions))
    answers_length: tp.List[AnswerLength] = field(default_factory=lambda: [AnswerLength.SHORT] * (GeneratorConfig.number_of_questions))
    answers_token: AnswerToken = AnswerToken.BIG_LETTERS
    answers_separator: AnswerSeparator = AnswerSeparator.CLOSE_PARENTHESIS

    # Others
    check_mark_type: MarkType = MarkType.CIRCLE
    uncheck_mark_type: MarkType = MarkType.CROSS

    @staticmethod
    def random():
        number_of_questions = random.randint(*NUMBER_OF_QUESTIONS_RANGE)
        check_mark_type, uncheck_mark_type = GeneratorConfig.__random_marks()

        return GeneratorConfig(
            font=random.choice(list(Font)),
            font_size=random.randint(*FONT_SIZE_RANGE),

            rule_structures=random.sample(list(RuleStructure), len(list(RuleStructure))),

            number_of_questions=number_of_questions,
            questions_length=[random.choice(list(QuestionLength)) for _ in range(number_of_questions)],

            number_of_answers=[random.randint(*NUMBER_OF_ANSWERS_RANGE) for _ in range(number_of_questions)],
            answers_layout=[random.choice(list(AnswerLayout)) for _ in range(number_of_questions)],
            answers_length=[random.choice(list(AnswerLength)) for _ in range(number_of_questions)],
            answers_token=random.choice(list(AnswerToken)),
            answers_separator=random.choice(list(AnswerSeparator)),

            check_mark_type=check_mark_type,
            uncheck_mark_type=uncheck_mark_type
        )

    @staticmethod
    def __random_marks() -> tp.Tuple[MarkType, MarkType]:
        check_mark_type = random.choice(list(MarkType))
        uncheck_mark_type = random.choice(list(MarkType))
        if MarkType.is_valid(check_mark_type, uncheck_mark_type):
            return check_mark_type, uncheck_mark_type
        else:
            return GeneratorConfig.__random_marks()
