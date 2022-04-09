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

    def is_valid(check_mark: MarkType, uncheck_mark: MarkType) -> bool:
        if check_mark == uncheck_mark or uncheck_mark == MarkType.UNDERSCORE or (check_mark, uncheck_mark) == (MarkType.DOODLE, MarkType.CROSS):
            return False
        return True


class RuleStructures(IntEnum):
    DESCRIPTION = 0
    INDEKS = auto()
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


class AnswerLenght(IntEnum):
    SHORT = 5
    MEDIUM = 10
    LONG = 50


class AnswerToken(Enum):
    # Value are set as first elements from list of tokens

    SMALL_LETTERS = "A"     # A B C
    BIG_LETTERS = "a"       # a b c
    NUMBERS = "1"           # 1 2 3
    ROMAN_NUMBERS = "I"     # I II III
    DOTS = "•"              # • • •
    DASH = "-"              # - - -


class AnswerSeparator(Enum):
    DOT = "."               # .
    CLOSE_PARENTHESIS = ")" # )
    PIPE = "|"              # |
    COLON = ":"             # :
    SEMICOLON = ";"         # ;
    SPACE = " "             # [[:space:]]
    SLASH = "/"             # /
    BACKSLASH = "\\"        # \



@dataclass
class GeneratorConfig:
    # Document style
    font: Font = Font.TERMES
    font_size: int = 11

    # Rule section
    rule_description: str = "Example description"
    rule_structure: tp.List[RuleStructures] = field(default_factory= lambda: list(RuleStructures)) # get every member of RuleStructures as int

    # Question sections
    number_of_questions: int = 6
    answers_layout: tp.List[RuleStructures] = field(default_factory=lambda: [AnswerLayout.ONE_COLUMN] * (GeneratorConfig.number_of_questions))
    answers_length: tp.List[AnswerLenght] = field(default_factory=lambda: [AnswerLenght.SHORT] * (GeneratorConfig.number_of_questions))
    number_of_answers: tp.List[int] = field(default_factory=lambda: [4] * (GeneratorConfig.number_of_questions))
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
            font = random.choice(list(Font)),
            font_size = random.randint(*FONT_SIZE_RANGE),

            rule_structure = random.shuffle(list(RuleStructures)),

            number_of_questions = number_of_questions,
            answers_layout = [random.choice(list(AnswerLayout)) for _ in range(number_of_questions)],
            answers_length = [random.choice(list(AnswerLenght)) for _ in range(number_of_questions)],
            number_of_answers = [random.choice(list(AnswerLenght)) for _ in range(number_of_questions)],
            answers_token = random.choice(list(AnswerToken)),
            answers_separator = random.choice(list(AnswerSeparator)),

            check_mark_type = random.choice(list(MarkType)),
            uncheck_mark_type = random.choice(list(MarkType))
        )

    @staticmethod
    def __random_marks() -> tp.Tuple(MarkType, MarkType):
        check_mark_type = random.choice(list(MarkType))
        uncheck_mark_type = random.choice(list(MarkType))
        # TODO check if valid
