import io
import json
import logging
import typing as tp
from PIL import Image

import numpy as np
import requests

from src.config import Config


class ExamStorage:
    URL = "http://localhost:8888"

    @staticmethod
    def get_exams_names(exam_path: str):
        response = ExamStorage._send_request('GET', exam_path)
        return [file_data['name'] for file_data in response.json() if file_data['type'] == 'file']

    @staticmethod
    def get_answer_key_image(exam_path: str):
        return ExamStorage.get_exam_image(exam_path, 'answer_key.jpeg')

    @staticmethod
    def get_exam_image(exam_path: str, exam_name: str):
        response = ExamStorage._send_request('GET', ExamStorage._create_full_path(exam_path, exam_name))
        pil_image = Image.open(io.BytesIO(response.content))
        return np.asarray(pil_image)

    @staticmethod
    def set_answer_key_json(exam_path: str, json_value: tp.Dict):
        ExamStorage.set_exam_answer_json(exam_path, 'answer_key.json', json_value)

    @staticmethod
    def set_exam_answer_json(exam_path: str, exam_name: str, json_value: tp.Dict):
        exam_name = f'{exam_name}.json' if not exam_name.endswith('.json') else exam_name
        full_path = ExamStorage._create_full_path(exam_path, exam_name)
        ExamStorage._send_request('PUT', full_path, json.dumps(json_value).encode())

    @staticmethod
    def _create_full_path(exam_path: str, exam_name: str):
        return f'{exam_path}{"/" if not exam_path.endswith("/") else ""}{exam_name}'

    @staticmethod
    def _send_request(method: str, path: str, data: tp.Any = None) -> requests.Response:
        url = f'{ExamStorage.URL}{path}'
        response = requests.request(method, url, data=data)
        if not response.ok:
            logging.error(f"Can't connect to exam storage server (method={method}, path={path})")
            raise requests.ConnectionError
        return response


if __name__ == '__main__':
    ExamStorage.set_exam_answer_json('/', 'test3', {'foo': 'bar'})
    ExamStorage.get_exam_image('/', 'test2')
    ExamStorage.get_exams_names('/')
