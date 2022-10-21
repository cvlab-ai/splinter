from importlib.metadata import metadata
import io
import json
import typing as tp
from pathlib import Path

import numpy as np
import requests
from PIL import Image
from src.config import Config
import pdf2image
from src.pdf import PDFType
import enum


class Metadata(enum.Enum):
    pdfs_done = 1


class Storage:
    @staticmethod
    def get_output_path(exam_id: int, pdf_type: PDFType):
        if pdf_type == PDFType.answer_sheets:
            return Storage.get_student_dir(exam_id)
        elif pdf_type == PDFType.answer_keys:
            return Storage.get_answer_key_dir(exam_id)

    @staticmethod
    def get_input_path(exam_id: int, pdf_type: PDFType):
        if pdf_type == PDFType.answer_sheets:
            return Storage.get_answer_sheet_pdfs_dir(exam_id)
        elif pdf_type == PDFType.answer_keys:
            return Storage.get_answer_key_dir(exam_id)

    @staticmethod
    def get_answer_key_dir(exam_id):
        return f"{exam_id}/{Config.exam_storage.answer_keys_dir}/"

    @staticmethod
    def get_answer_sheet_pdfs_dir(exam_id):
        return f"{exam_id}/{Config.exam_storage.default_input_dirname}/"

    @staticmethod
    def get_student_dir(exam_id, index=None):
        if index:
            return f"{exam_id}/{Config.exam_storage.default_output_dirname}/{index}"
        else:
            return f"{exam_id}/{Config.exam_storage.default_output_dirname}"

    @staticmethod
    def get_metadata(exam_id: int):
        metadata_json = Storage.get_file(
            f"{exam_id}/{Config.exam_storage.metadata_filename}"
        )
        if metadata_json is None:
            metadata_json = {Metadata.pdfs_done.name: {t.name: [] for t in PDFType}}
        else:
            metadata_json = metadata_json.json()
            for key in Metadata:
                if key.name not in metadata_json:
                    metadata_json[key.name] = {}

            # init pdf metadata
            for pdf_type in PDFType:
                if pdf_type.name not in metadata_json[Metadata.pdfs_done.name]:
                    metadata_json[Metadata.pdfs_done.name][pdf_type.name] = []
        return metadata_json

    @staticmethod
    def unpack_pdf(file_path: str):
        response = Storage.get_file(file_path)
        if response is None:
            return None
        return pdf2image.convert_from_bytes(response.content)

    @staticmethod
    def get_pdfs_names(exam_id: str, pdf_type: PDFType) -> tp.List[str]:
        if pdf_type == PDFType.answer_sheets:
            dir = Storage._get_dir(Storage.get_answer_sheet_pdfs_dir(exam_id))
        elif pdf_type == PDFType.answer_keys:
            dir = Storage._get_dir(Storage.get_answer_key_dir(exam_id))
        if dir is None:
            return None
        return [
            file_data["name"]
            for file_data in dir
            if file_data["type"] == "file"
            and file_data["name"].endswith(Config.exam_storage.img_extension)
        ]

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
    def push_dir(local_dir: Path, remote_dir: str, recursive=False):
        for file in local_dir.iterdir():
            if file.is_file():
                Storage._send_request(
                    "PUT", f"{remote_dir}/{file.name}", data=open(file, "rb")
                )
            if file.is_dir() and recursive:
                Storage.push_dir(file, f"{remote_dir}/{file.name}")
        pass

    @staticmethod
    def push_student_dir(exam_id: int, student_dir: Path):
        for filepath in student_dir.iterdir():
            Storage._send_request(
                "PUT",
                f"{exam_id}/{Config.exam_storage.default_output_dirname}/{student_dir.name}/{filepath.name}",
                data=open(filepath, "rb"),
            )

    @staticmethod
    def get_exam_image(
        exam_path: str,
        exam_name: str,
    ) -> np.ndarray:
        path = Storage._create_full_path(exam_path, exam_name)
        response = Storage._send_request("GET", path)
        pil_image = Image.open(io.BytesIO(response.content))
        return np.asarray(pil_image)

    @staticmethod
    def set_exam_answer_json(exam_path: str, exam_name: str, json_value: tp.Dict):
        filename = Storage.change_extension(exam_name, "json")
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


if __name__ == "__main__":
    Storage.set_exam_answer_json("/exam1", "test_exam1", {"foo": "bar"})
    exam_img = Storage.get_exam_image("/exam1", "test_exam1")
    exams_names = Storage.get_pdfs_names("exams/")
