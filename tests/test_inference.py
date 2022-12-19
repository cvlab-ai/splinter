import os
from pathlib import Path
import tempfile
import json

import splinter


SCRIPT_DIR = Path(os.path.realpath(os.path.dirname(__file__)))

def test_check_exam(inf_engine: splinter.InfEngine, exam_storage: splinter.ExamStorage, test_exam_id: int):
    inf_engine.check_exam(test_exam_id)
    assert exam_storage.splinter.check(f'/{test_exam_id}/answers_keys/answers_b_1.json'), "Answers key should be generated."
    assert exam_storage.splinter.check(f'/{test_exam_id}/students/654321/answers_1.json'), "Student's answers should be recognized"
    assert exam_storage.splinter.check(f'/{test_exam_id}/scores.csv'), "The exam summary scores should be calculated"


def test_check_exam_force(inf_engine: splinter.InfEngine, exam_storage: splinter.ExamStorage, test_exam_id: int):
    inf_engine.check_exam(test_exam_id)
    inf_engine.check_exam(test_exam_id, force=True)
    anwers_dir = exam_storage.splinter.list(f"{test_exam_id}/students/654321/")
    assert len([ans for ans in anwers_dir if '.json' in ans]) == 2, "Student's answer should be checked twice after force"


def test_answer_inference(inf_engine: splinter.InfEngine, exam_storage: splinter.ExamStorage, test_exam_id: int):
    inf_engine.check_exam(test_exam_id)
    with tempfile.TemporaryDirectory() as tmp, Path(tmp) as tmp_dir:
        exam_storage.splinter.download_sync(remote_path=f'/{test_exam_id}/students/654321/answers_1.json', local_path=tmp_dir/'answers_1.json')
        with open(SCRIPT_DIR/'test_data/expected/answers/answers_1.json') as exp, open(tmp_dir/'answers_1.json') as test:
            assert json.load(exp) == json.load(test), "Recognized student's answers as expected"


def test_key_inference(inf_engine: splinter.InfEngine, exam_storage: splinter.ExamStorage, test_exam_id: int):
    inf_engine.check_exam(test_exam_id)
    with tempfile.TemporaryDirectory() as tmp, Path(tmp) as tmp_dir:
        exam_storage.splinter.download_sync(remote_path=f'/{test_exam_id}/answers_keys/answers_b_1.json', local_path=tmp_dir/'answers_b_1.json')
        with open(SCRIPT_DIR/'test_data/expected/keys/answers_b_1.json') as exp, open(tmp_dir/'answers_b_1.json') as test:
            assert json.load(exp) == json.load(test), "Recognized student's answers as expected"
