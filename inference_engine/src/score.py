import enum
import csv
import typing as tp
from src.exam_storage import versioning


class ScrStrtg(enum.Enum):
    AC = 0  # all correct
    PC = 1  # partial correct


class ScoreCSV:
    file: tp.IO = None
    writer = None

    def __init__(self, file: tp.IO):
        self.file = file
        self.writer = csv.writer(self.file)

    def write_scores(self, results: tp.List[tp.Any], answer_keys):
        if results is None:
            return
        if not len(results):
            return

        #### header ####
        number_of_question = len(results[0]["answers"])
        number_of_answers = len(results[0]["answers"]["1"])
        header = ["Student ID", "Group", "Result AC", "Result PC"]
        for question_number in range(number_of_question):
            for answer_number in range(number_of_answers):
                header.extend([f"Q{question_number+1}A{answer_number+1}"])
        self.writer.writerow(header)

        #### answers keys ####
        for group in answer_keys:
            answer_sum = sum_answered_questions(answer_keys[group]["answers"])
            answer_key_row = ["Answer Key", group, answer_sum, answer_sum]
            for answer in answer_keys[group]["answers"]:  # iter over questions
                for a in answer_keys[group]["answers"][
                    answer
                ]:  # iter over answers in question
                    answer_key_row.append(a)
            self.writer.writerow(answer_key_row)

        #### students ####
        for result in results:  # iter over students
            group = versioning.examkey2group(result["exam_key"])
            if group in answer_keys:
                student_row = [
                    result["student_id_boxes"],
                    group,
                    calc_student_score(result, answer_keys[group], ScrStrtg.AC),
                    calc_student_score(result, answer_keys[group], ScrStrtg.PC),
                ]
            else:
                student_row = [result["student_id_boxes"], "NO GROUP", 0, 0]

            for answer in result["answers"]:  # iter over questions
                for a in result["answers"][answer]:  # iter over answers in question
                    student_row.append(a)
            self.writer.writerow(student_row)


def sum_answered_questions(answers):
    if answers is None:
        return 0
    question_sum = 0
    for answer in answers:
        if sum(answers[answer]):
            question_sum += 1
    return question_sum


def calc_student_score(result, answers_key, scoring_system: ScrStrtg = ScrStrtg.AC):
    score = 0
    if scoring_system == ScrStrtg.AC:
        for answer in result["answers"]:
            if 1 in answers_key["answers"][answer]:
                score += result["answers"][answer] == answers_key["answers"][answer]
    elif scoring_system == ScrStrtg.PC:
        for answer in result["answers"]:
            q_score = 0
            q_max = sum(answers_key["answers"][answer])
            if q_max == 0:
                continue
            for i, a in enumerate(result["answers"][answer]):
                if answers_key["answers"][answer][i]:
                    if a == answers_key["answers"][answer][i]:
                        q_score += 1
                elif a == 1:
                    q_score -= 1
            score += max([0, q_score / q_max])

    return score
