import io
import json
import typing as tp
from PIL import Image

import numpy as np
import requests

from src.config import Config


class Storage:
    @staticmethod
    def get_exams_names(exam_path: str) -> tp.List[str]:
        path = Storage._create_full_path(exam_path, '')
        response = Storage._send_request("GET", path)
        return [file_data["name"] for file_data in response.json() if file_data["type"] == "file"
                and file_data["name"].endswith(Config.exam_storage.img_extension)]

    @staticmethod
    def get_exam_image(exam_path: str, exam_name: str, ) -> np.ndarray:
        path = Storage._create_full_path(exam_path, exam_name)
        response = Storage._send_request("GET", path)
        pil_image = Image.open(io.BytesIO(response.content))
        return np.asarray(pil_image)

    @staticmethod
    def set_exam_answer_json(exam_path: str, exam_name: str, json_value: tp.Dict):
        filename = Storage.change_extension(exam_name, 'json')
        path = Storage._create_full_path(exam_path, filename)
        Storage._send_request("PUT", path, json.dumps(json_value).encode())

    @staticmethod
    def change_extension(filename: str, extension: str):
        return f"{filename.split('.')[0]}.{extension}"

    @staticmethod
    def _create_full_path(exam_path: str, exam_name: str):
        return f"{exam_path}/{exam_name}"

    @staticmethod
    def _send_request(method: str, path: str, data: tp.Any = None) -> requests.Response:
        url = f"{Config.exam_storage.full_url}/{path}"
        response = requests.request(method, url, data=data)
        if not response.ok:
            raise requests.ConnectionError(url, response.status_code)
        return response


if __name__ == "__main__":
    Storage.set_exam_answer_json("/exam1", "test_exam1", {"foo": "bar"})
    exam_img = Storage.get_exam_image("/exam1", "test_exam1")
    exams_names = Storage.get_exams_names("exams/")
