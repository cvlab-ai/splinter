from . import GeneratorConfig
from .logger import logger
from .generator_config import AnswerLayout, AnswerSeparator, AnswerToken


class RuleGenerator:
    def __init__(self, config: GeneratorConfig):
        self.config = config


############ QUESTION GENERATION #############
import pylatex as ptex
import lorem
from .utils import int_to_roman


class QuestionGenerator:
    def __init__(self, config: GeneratorConfig):
        self.config = config

    def generate(self):
        questions = []
        for i in range(self.config.number_of_questions):
            questions.append(self.__generate_single_question(self.config.answers_layout[i],
                                                             self.config.number_of_answers[i],
                                                             self.config.answers_token,
                                                             self.config.answers_separator))
        return questions

    @staticmethod
    def __generate_single_question(answer_layout: AnswerLayout, number_of_answers: int, answer_token: AnswerToken, answer_sep: AnswerSeparator):
        section = ptex.Section(f"{lorem.sentence()}")
        # question_content = ptex.Subsection("")
        # question_content.append(lorem.sentence())
        # logger.debug(f"Generated question: {question_content}")

        answers = ptex.Description()
        logger.debug(f"Token: {answer_token}")

        for token in QuestionGenerator.__token_generator(answer_token, number_of_answers):
            answers.add_item(f"{token}{answer_sep.value}",f"{lorem.sentence()}")
            logger.debug(f"Generated answer: {token}{answer_sep.value} {lorem.sentence()}")

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
        # doc = ptex.Document('basic', font_size=self.config.font_size)
        doc = ptex.Document()
        doc.documentclass = ptex.Command(
            "documentclass",
            options=[f"{self.config.font_size}pt"],
            arguments=["article"],
        )

        question_generator = QuestionGenerator(self.config)
        for question in question_generator.generate():
            doc.append(question)

        # doc.generate_pdf("exam", clean_tex=False)
        doc.generate_tex()

    def generate_multiple(self, count: int):
        exams = []
        for _ in range(count):
            exams.append(self.generate())

        return exams
