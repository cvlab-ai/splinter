from __future__ import annotations

import json
import random
import typing as tp
import uuid
from dataclasses import dataclass, field, asdict
from enum import Enum, IntEnum, auto

from .utils import random_date
from .config import *


class Font(Enum):
    MODERN = "lmodern"
    KPFONTS = "kpfonts"
    GFSDIDOT = "gfsartemisia"
    UTOPIA = "fourier"
    VENTURIS = "venturis"
    LIBERTINE = "libertine"
    TERMES = "tgtermes"


class MarkType(str, Enum):
    CIRCLE = "Zakreśl"
    CROSS = "Przekreśl krzyżykiem"
    DOODLE = "Zamaż"
    UNDERSCORE = "Podkreśl"

    @staticmethod
    def is_valid(check_mark: MarkType, uncheck_mark: MarkType) -> bool:
        if any(
            [
                check_mark == uncheck_mark,
                uncheck_mark == MarkType.UNDERSCORE,
                (check_mark, uncheck_mark) == (MarkType.DOODLE, MarkType.CROSS),
            ]
        ):
            return False
        return True


class RuleStructure(IntEnum):
    DATE = 0
    INDEX = auto()
    DESCRIPTION = auto()
    EXAM_DURATION = auto()
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
    BIG_LETTERS = "A"  # A B C
    SMALL_LETTERS = "a"  # a b c
    NUMBERS = "1"  # 1 2 3
    ROMAN_NUMBERS = "I"  # I II III
    DOTS = "•"  # • • •
    DASH = "-"  # - - -


class AnswerSeparator(Enum):
    DOT = "."
    CLOSE_PARENTHESIS = ")"
    CLOSE_BRACKET = "]"
    PIPE = "|"
    COLON = ":"
    SPACE = " "


@dataclass
class GeneratorConfig:
    # Document style
    font: Font = Font.TERMES
    font_size: int = 10
    top_margin: float = 1.0  # cm
    left_margin: float = 2.0  # cm
    answer_interline: int = 0
    question_interline: int = 5

    # Question sections
    number_of_questions: int = 6

    questions_length: tp.List[QuestionLength] = field(
        default_factory=lambda: [QuestionLength.MEDIUM]
        * GeneratorConfig.number_of_questions
    )

    number_of_answers: tp.List[int] = field(
        default_factory=lambda: [4] * GeneratorConfig.number_of_questions
    )

    answers_layout: tp.List[AnswerLayout] = field(
        default_factory=lambda: [AnswerLayout.ONE_COLUMN]
        * GeneratorConfig.number_of_questions
    )

    answers_length: tp.List[AnswerLength] = field(
        default_factory=lambda: [AnswerLength.SHORT]
        * GeneratorConfig.number_of_questions
    )

    answers_token: AnswerToken = AnswerToken.BIG_LETTERS
    answers_separator: AnswerSeparator = AnswerSeparator.CLOSE_PARENTHESIS
    check_mark_type: MarkType = MarkType.CIRCLE
    uncheck_mark_type: MarkType = MarkType.CROSS

    # Rule section
    rule_structures: tp.List[RuleStructure] = field(
        default_factory=lambda: list(RuleStructure)
    )  # get every member of RuleStructure as int
    rule_section_title: str = "Egzamin z przedmiotu \"Systemy z uczeniem maszynowym\""
    rule_title_font_size = 5

    rule_exam_duration: int = 45
    rule_max_points_per_question: int = 4
    rule_exam_date: str = "20.05.2022"
    rules_interline: int = 5
    rule_index_box_size = (80, 15)

    # Others
    exam_id: str = field(default_factory=lambda: int(uuid.uuid4()))

    @staticmethod
    def random():
        number_of_questions = random.randint(*NUMBER_OF_QUESTIONS_RANGE)
        check_mark_type, uncheck_mark_type = GeneratorConfig.__random_marks()
        token, separator = GeneratorConfig.__random_token_separator()

        return GeneratorConfig(
            font=random.choice(list(Font)),
            font_size=random.randint(*FONT_SIZE_RANGE),
            top_margin=round(random.uniform(*TOP_MARGIN_RANGE), 1),
            left_margin=round(random.uniform(*LEFT_MARGIN_RANGE), 1),
            answer_interline=random.randint(*ANSWER_INTERLINE_RANGE),
            question_interline=random.randint(*QUESTION_INTERLINE_RANGE),

            rule_structures=random.sample(
                list(RuleStructure), len(list(RuleStructure))
            ),
            rule_exam_date=random_date(EXAM_DATE_RANGE[0], EXAM_DATE_RANGE[1], random.random()),

            number_of_questions=number_of_questions,
            questions_length=[
                random.choice(list(QuestionLength)) for _ in range(number_of_questions)
            ],
            number_of_answers=[
                random.randint(*NUMBER_OF_ANSWERS_RANGE)
                for _ in range(number_of_questions)
            ],
            answers_layout=[
                random.choice(list(AnswerLayout)) for _ in range(number_of_questions)
            ],
            answers_length=[
                random.choice(list(AnswerLength)) for _ in range(number_of_questions)
            ],
            answers_token=token,
            answers_separator=separator,
            check_mark_type=check_mark_type,
            uncheck_mark_type=uncheck_mark_type,
        )

    @staticmethod
    def __random_marks() -> tp.Tuple[MarkType, MarkType]:
        check_mark_type = random.choice(list(MarkType))
        uncheck_mark_type = random.choice(list(MarkType))
        if MarkType.is_valid(check_mark_type, uncheck_mark_type):
            return check_mark_type, uncheck_mark_type
        else:
            return GeneratorConfig.__random_marks()

    @staticmethod
    def __random_token_separator() -> tp.Tuple[AnswerToken, AnswerSeparator]:
        token = random.choice(list(AnswerToken))
        separator = random.choice(list(AnswerSeparator))
        if GeneratorConfig.__check_token_separator_validity(token, separator):
            return token, separator
        else:
            return GeneratorConfig.__random_token_separator()

    @staticmethod
    def __check_token_separator_validity(token: AnswerToken, separator: AnswerSeparator) -> bool:
        if token in [AnswerToken.DOTS, AnswerToken.DASH] and (separator != AnswerSeparator.SPACE):
            return False
        return True

    def export(self, filename: str):
        with open(filename, 'w') as f:
            json.dump(asdict(self), f, default=str, indent=4)
