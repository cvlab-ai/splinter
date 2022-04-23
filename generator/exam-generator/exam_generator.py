from . import GeneratorConfig
from .text_generator import TextGenerator
from .rule_generator import RuleGenerator
from .logger import logger
from .generator_config import AnswerLayout, QuestionLength, AnswerLength, AnswerSeparator, AnswerToken
from .exam_document import ExamDocument
from .answers import Answers



############ QUESTION GENERATION #############
import random

import pylatex as ptex
from .utils import int_to_roman


class QuestionGenerator:
    def __init__(self, config: GeneratorConfig):
        self.config = config

    def generate(self):
        questions = []
        for i in range(self.config.number_of_questions):
            questions.append(self.__generate_single_question(self.config.questions_length[i],
                                                             self.config.answers_layout[i],
                                                             self.config.answers_length[i],
                                                             self.config.number_of_answers[i]))
        return questions

    def __generate_single_question(self, question_length: QuestionLength, answer_layout: AnswerLayout, answer_length: AnswerLength, number_of_answers: int):
        question_text = TextGenerator.generate_question_text(random.randint(1, question_length))
        logger.debug(f"Generated Question: {question_text}")

        section = ptex.Section(f"{question_text}")
        answers = Answers()

        for token in QuestionGenerator.__token_generator(self.config.answers_token, number_of_answers):
            answer_text = TextGenerator.generate_text(random.randint(1, answer_length))
            answers.add_item(f"{token}{self.config.answers_separator.value}", answer_text)
            logger.debug(f"Generated answer: {token}{self.config.answers_separator.value} {answer_text}")

        section.append(answers)
        return section

    @staticmethod
    def __token_generator(answer_token: AnswerToken, number_of_answers: int):
        start_token = answer_token.value if answer_token != AnswerToken.ROMAN_NUMBERS else 1
        for i in range(number_of_answers):
            if answer_token in [AnswerToken.SMALL_LETTERS, AnswerToken.BIG_LETTERS]:
                yield chr(ord(start_token) + i)
            if answer_token == AnswerToken.NUMBERS:
                yield str(int(start_token) + i)
            if answer_token == AnswerToken.ROMAN_NUMBERS:
                yield int_to_roman(int(start_token) + i)
            if answer_token in [AnswerToken.DOTS, AnswerToken.DASH]:
                yield answer_token.value


class ExamGenerator:
    def __init__(self, config: GeneratorConfig):
        self.config = config

    def generate(self):
        logger.info("Generating exam...")
        doc = ExamDocument(self.config)

        rule_generator = RuleGenerator(self.config)
        doc.append(rule_generator.generate())

        question_generator = QuestionGenerator(self.config)
        for question in question_generator.generate():
            doc.append(ptex.NoEscape('{\\nobreak'))
            doc.append(question)
            doc.append(ptex.NoEscape('}'))

        doc.generate_tex("exam")
        doc.generate_pdf("exam", clean_tex=False)

    def generate_multiple(self, count: int):
        exams = []
        for _ in range(count):
            exams.append(self.generate())
        return exams
