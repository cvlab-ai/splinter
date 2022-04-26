from typing import List
from tabulate import tabulate
from random import choices, shuffle, randint

exam_marks = {"mark": "mark", "negation": "negation", "no mark": "no mark"}


def generate_key_sequence(
    answers_amount: int, mark_odd: float = 0.8, negated_odd: float = 0.25
) -> List[str]:
    """Generates sequence of answers in three types for single question
    Marked - requires to be marked with symbol
    Negated - requires to be marked and than negated
    No Mark - doesn't require any action, means to leave answer empty

    :param answers_amount: Refers to number of answers in particular question
    :type answers_amount: int
    :param mark_odd: Describes odds of getting answer marked, defaults to 0.8
    :type mark_odd: float, optional
    :param negated_odd: Describes odds of getting answer negated, defaults to 0.25
    :type negated_odd: float, optional
    :return: Returns combination of marked, negated and no mark with certain odds
    :rtype: List[str]
    """

    def generate_weights(amount: int, odds: float) -> List[float]:
        """Generates weights for further answers randomization

        :param amount: Amounts of weights to be chosen
        :type amount: int
        :param odds: Odds that are used as multiplier for weights
        :type odds: float
        :return: Contains weights normalized to 1
        :rtype: List[float]
        """
        weights = []
        for odds_index in range(amount):
            weights.append(odds**odds_index)
        odds_multiplier = 1 / sum(weights)
        weights = [weight * odds_multiplier for weight in weights]
        if sum(weights) != 1:
            weights[0] += 1 - sum(weights)
        assert sum(weights) == 1
        return weights

    assert answers_amount >= 2, "Incorect amount of answers"
    assert 0 < mark_odd < 1 and 0 < negated_odd < 1, "Incorrect odds"

    positive_odds = generate_weights(answers_amount, mark_odd)
    population_positive = list(range(1, answers_amount + 1))
    positive_answers = choices(population_positive, positive_odds, k=1)[0]
    negative_odds = generate_weights(positive_answers, negated_odd)
    population_negative = list(range(0, positive_answers))
    negations = choices(population_negative, negative_odds, k=1)[0]
    no_mark = answers_amount - positive_answers
    positive_answers -= negations

    assert (
        no_mark + positive_answers + negations == answers_amount
    ), "Invalid mark count"
    answers_array = (
        [exam_marks["mark"]] * positive_answers
        + [exam_marks["negation"]] * negations
        + [exam_marks["no mark"]] * no_mark
    )
    shuffle(answers_array)
    return answers_array


def generate_exam_helper(answers_number: List[int]) -> List[List[str]]:
    """Function responsible for generating instruction for exam

    :param answers_number: List of numbers of answers for each question
    :type answers_number: List[int]
    :return: List containing sequences of required marks
    :rtype: List[List[str]]
    """

    def pad_with_spaces(table: List[List[str]]) -> List[List[str]]:
        """Adds padding behind answers to make them look alligned in table

        :param table:
        :type table: List[List[str]]
        :return: Exam padded to longest answer sequence
        :rtype: List[List[str]]
        """
        max_answers = max([len(question) for question in table])
        return [question + [" "] * (max_answers - len(question)) for question in table]

    exam = [generate_key_sequence(answer_number) for answer_number in answers_number]
    exam = pad_with_spaces(exam)
    exam = add_question_numbers(exam)
    return exam


def add_question_numbers(table: List[List[str]]) -> List[List[str]]:
    """Adds in front of answers number of reffering question

    :param table: Table containing sequences of answers for each question
    :type table: List[List[str]]
    :return: Sequences of answers prepended with question index number
    :rtype: List[List[str]]
    """
    return [[f"Question {idx + 1}"] + answers for idx, answers in enumerate(table)]


def save_to_file(path: str, exam: List[str]) -> bool:
    """Saves instruction to file

    :param path: System relative path
    :type path: str
    :param exam: Table of sequences of answers
    :type exam: List[str]
    :return: Returns status if any characters written to file
    :rtype: bool
    """
    with open(path, "w+") as file:
        characters_written = file.write(exam)
    return bool(characters_written)


def tabulate_answers(exam: List[List[str]]) -> List[List[str]]:
    """Converts list to ascii table

    :param exam: List of answers sequences
    :type exam: List[List[str]]
    :return: Tabulated sequence of answers sequences
    :rtype: List[List[str]]
    """
    headers = [" "] + [f"Answer {idx + 1}" for idx in range(len(exam))]
    return tabulate(exam, headers=headers, tablefmt="github")


def generate_exam_instruction(amount_of_answers: List[int], path: str) -> bool:
    """Run pipeline to create answers for particular exam

    :param amount_of_answers: Contains amount of answers per questions
    :type amount_of_answers: List[int]
    :param path: Path for file to be saved to
    :type path: str
    :return: Status on file save
    :rtype: bool
    """
    exam = generate_exam_helper(amount_of_answers)
    return bool(save_to_file(path, tabulate_answers(exam)))
