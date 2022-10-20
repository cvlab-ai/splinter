import io
import json
import typing as tp
from pathlib import Path

import numpy as np
import requests
from PIL import Image
from src.config import Config


class Storage:
    @staticmethod
    def get_pdfs_names(exam_id: str) -> tp.List[str]:
        dir = Storage._get_dir(f"{exam_id}/{Config.exam_storage.default_input_dirname}/")
        return [file_data["name"] for file_data in dir if file_data["type"] == "file"
                and file_data["name"].endswith(Config.exam_storage.img_extension)]

    @staticmethod
    def get_file(file_path: str):
        try:
            return Storage._send_request("GET", file_path)
        except requests.ConnectionError as e:
            if e.args[1] == 404:
                return None
            raise

    @staticmethod
    def put_file(file_path: str, data: tp.Any):
        Storage._send_request("PUT", file_path, data=data)

    @staticmethod
    def next_answer_version(exam_id: int, index: str):

        dir_content = Storage._get_dir(f"{exam_id}/{Config.exam_storage.default_output_dirname}/{index}/")
        if dir_content is None:
            return 0
        version_candidates = Storage._filter_versioned_files([row['name'] for row in dir_content])
        return Storage._find_next_file_version(version_candidates)

    @staticmethod
    def push_student_dir(exam_id: int, student_dir: Path):
        for filepath in student_dir.iterdir():
            Storage._send_request("PUT", f"{exam_id}/{Config.exam_storage.default_output_dirname}/{student_dir.name}/{filepath.name}", data=open(filepath, "rb"))

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
        response = requests.request(
            method,
            url,
            data=data,
            auth=requests.auth.HTTPBasicAuth(
                Config.exam_storage.exam_storage_user,
                Config.exam_storage.exam_storage_password,
            ),
        )
        if not response.ok:
            raise requests.ConnectionError(url, response.status_code)
        return response

    @staticmethod
    def _get_dir(dirpath: str):
        try:
            response = Storage._send_request("GET", f"{dirpath}/")
        except requests.ConnectionError as e:
            if e.args[1] == 404:
                return None
            raise
        return response.json()

    @staticmethod
    def _filter_versioned_files(files, base_filename='answers', ext='json'):
        names = []
        for filename in files:
            name, ext = filename.split('.', 1)
            if ext == 'json' and name.startswith(base_filename):
                names.append(name)
        return names

    @staticmethod
    def _find_next_file_version(files):
        if len(files) == 0:
            return 0
        latest_name = max(files)
        version = latest_name.split('_')[-1]
        if version.isnumeric():
            return int(version) + 1
        # some files exist but without version,
        # that means next one should be versioned
        return 1


if __name__ == "__main__":
    Storage.set_exam_answer_json("/exam1", "test_exam1", {"foo": "bar"})
    exam_img = Storage.get_exam_image("/exam1", "test_exam1")
    exams_names = Storage.get_pdfs_names("exams/")
