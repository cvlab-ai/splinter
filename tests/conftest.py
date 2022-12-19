import os
from pathlib import Path
from dotenv import load_dotenv
import pytest

import splinter

SCRIPT_DIR = Path(os.path.realpath(os.path.dirname(__file__)))
ENV_FILE = SCRIPT_DIR / '../.env'
TEST_EXAM_ID = 1


def pytest_configure(config):
    load_dotenv(ENV_FILE)


def pytest_unconfigure(config):
    exam_storage = splinter.ExamStorage()
    exam_storage.clean_splinter()


@pytest.fixture
def inf_engine():
    inf_engine = splinter.InfEngine()
    return inf_engine


@pytest.fixture
def exam_storage():
    exam_storage = splinter.ExamStorage()
    return exam_storage

@pytest.fixture
def test_exam_id():
    return TEST_EXAM_ID

@pytest.fixture(autouse=True)
def init_exam_storage(exam_storage: splinter.ExamStorage):
    exam_storage.clean_splinter()
    exam_storage.splinter.mkdir(f'/{TEST_EXAM_ID}')
    exam_storage.splinter.upload_sync(remote_path=f'/{TEST_EXAM_ID}/pdfs/', local_path=SCRIPT_DIR/'test_data/answers/')
    exam_storage.splinter.upload_sync(remote_path=f'/{TEST_EXAM_ID}/answers_keys/', local_path=SCRIPT_DIR/'test_data/keys/')
