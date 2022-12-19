import io
import json
import typing as tp
from pathlib import Path

import numpy as np
import pdf2image
import requests
from PIL.Image import Image
from src.config.config import Config
from src.exam_storage.pdf_type import PDFType
from typing import Optional
import logging
from  src.exam_storage import versioning


def get_file(file_path: str) -> Optional[requests.Response]:
    try:
        return _send_request("GET", file_path)
    except requests.ConnectionError as e:
        if e.args[1] == 404:
            return None
        raise


def put_file(file_path: str, data: tp.Any):
    _send_request("PUT", file_path, data=data)


def push_dir(local_dir: Path, remote_dir: str, recursive=False):
    for file in local_dir.iterdir():
        if file.is_file():
            _send_request("PUT", f"{remote_dir}/{file.name}", data=open(file, "rb"))
        if file.is_dir() and recursive:
            push_dir(file, f"{remote_dir}/{file.name}")
    pass


def push_student_dir(exam_id: int, student_dir: Path):
    for filepath in student_dir.iterdir():
        _send_request(
            "PUT",
            f"{exam_id}/{Config.exam_storage.default_output_dirname}/{student_dir.name}/{filepath.name}",
            data=open(filepath, "rb"),
        )


def get_exam_image(
    exam_path: str,
    exam_name: str,
) -> np.ndarray:
    path = _create_full_path(exam_path, exam_name)
    response = _send_request("GET", path)
    pil_image = Image.open(io.BytesIO(response.content))
    return np.asarray(pil_image)


def set_exam_answer_json(exam_path: str, exam_name: str, json_value: tp.Dict):
    filename = change_extension(exam_name, "json")
    path = _create_full_path(exam_path, filename)
    _send_request("PUT", path, json.dumps(json_value).encode())


def get_output_path(exam_id: int, pdf_type: PDFType):
    if pdf_type == PDFType.answer_sheets:
        return get_student_dir(exam_id)
    elif pdf_type == PDFType.answer_keys:
        return get_answer_key_dir(exam_id)


def get_input_path(exam_id: int, pdf_type: PDFType):
    if pdf_type == PDFType.answer_sheets:
        return get_answer_sheet_pdfs_dir(exam_id)
    elif pdf_type == PDFType.answer_keys:
        return get_answer_key_dir(exam_id)


def get_answer_key_dir(exam_id):
    return f"{exam_id}/{Config.exam_storage.answer_keys_dir}/"


def get_answer_sheet_pdfs_dir(exam_id):
    return f"{exam_id}/{Config.exam_storage.default_input_dirname}/"


def get_student_dir(exam_id, index=None):
    if index:
        return f"{exam_id}/{Config.exam_storage.default_output_dirname}/{index}"
    else:
        return f"{exam_id}/{Config.exam_storage.default_output_dirname}"


def unpack_pdf(file_path: str):
    response = get_file(file_path)
    if response is None:
        return None
    return pdf2image.convert_from_bytes(response.content)


def get_pdfs_names(exam_id: str, pdf_type: PDFType) -> tp.List[str]:
    if pdf_type == PDFType.answer_sheets:
        dir = get_dir(get_answer_sheet_pdfs_dir(exam_id))
    elif pdf_type == PDFType.answer_keys:
        dir = get_dir(get_answer_key_dir(exam_id))
    if dir is None:
        return None
    return [
        file_data["name"]
        for file_data in dir
        if file_data["type"] == "file"
        and file_data["name"].endswith(Config.exam_storage.img_extension)
    ]


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


def get_dir(dirpath: str):
    try:
        response = _send_request("GET", f"{dirpath}/")
    except requests.ConnectionError as e:
        if e.args[1] == 404:
            return None
        raise
    return response.json()


def _create_full_path(exam_path: str, exam_name: str):
    return f"{exam_path}/{exam_name}"


def change_extension(filename: str, extension: str):
    return f"{filename.split('.')[0]}.{extension}"


def get_students_results(exam_id) -> tp.List[tp.Any]:
    students_dir = get_dir(get_student_dir(exam_id))
    if students_dir is None:
        logging.info(f"Couldn't find checked students response in exam: {exam_id}")
        return None

    students_answers = []
    for folder in students_dir:
        if folder["type"] != "directory":
            continue
        student_dir_path = get_student_dir(exam_id) + "/" + folder["name"]
        latest_version = versioning.get_latest_remote_version(student_dir_path)
        answers_path = f"{student_dir_path}/{Config.exam_storage.result_basename}{versioning.v2s(latest_version)}.json"
        student_answers = get_file(answers_path)
        if student_answers is None:
            logging.warning(f"Couldn't open student answers: {answers_path}")
            continue
        students_answers.append(student_answers.json())

    return students_answers


def get_answer_keys(exam_id: int):
    answer_keys = {}
    if not (answer_key_dir := get_dir(get_answer_key_dir(exam_id))):
        return answer_keys

    groups = []
    for file in answer_key_dir:
        if file["type"] != "file":
            continue
        if not (file["name"].startswith("answers_") and file["name"].endswith(".json")):
            continue
        group = file["name"].split(".")[0].split("_")[1]
        groups.append(group)

    for group in groups:
        latest_version = versioning.get_latest_remote_version(f"{get_answer_key_dir(exam_id)}",sufix=f"_{group}")
        answer_key = get_file(f"{get_answer_key_dir(exam_id)}/{Config.exam_storage.result_basename}_{group}{versioning.v2s(latest_version)}.json")
        if answer_key is not None:
            answer_keys[group] = answer_key.json()
    return answer_keys
