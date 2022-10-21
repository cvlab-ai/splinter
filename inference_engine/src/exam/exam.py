import tempfile
import logging
import json
import numpy as np
import typing as tp
from PIL.Image import Image
from pathlib import Path

from src.storage import Storage
from src.config import Config
from src.pdf import PDFType
from . import versioning
from src.preprocessing import Preprocessing, Fields
from src.model import AnswerModel, OCRModel


def check_pdf(exam_id, file_name, pdf_type: PDFType, force=False):
    if not force and check_pdf_processed(exam_id, file_name, pdf_type):
        logging.info(f"PDF {file_name} already checked, skipping.")
        return
    with tempfile.TemporaryDirectory() as tmp, Path(tmp) as tmp_dir:
        images = Storage.unpack_pdf(
            f"{Storage.get_input_path(exam_id, pdf_type)}/{file_name}"
        )
        if images is None:
            logging.info(f"PDF {file_name} doesn't contains any images.")
            return
        for image in images:
            results = check_image(image)
            output_dir = tmp_dir
            if pdf_type == PDFType.answer_sheets:
                output_dir = output_dir / results[Fields.student_id]
                version = get_next_version(
                    output_dir,
                    Storage.get_student_dir(exam_id, index=results[Fields.student_id]),
                )
            elif pdf_type == PDFType.answer_keys:
                version = get_next_version(
                    output_dir, Storage.get_answer_key_dir(exam_id)
                )
            save_answers_to_dir(
                output_dir,
                results,
                version=version,
                image=image,
                add_exam_key_sufix=pdf_type == PDFType.answer_keys,
            )
        Storage.push_dir(
            tmp_dir, Storage.get_output_path(exam_id, pdf_type), recursive=True
        )
        mark_pdf_done(exam_id, file_name, pdf_type)


def check_pdf_processed(exam_id, file_name, pdf_type: PDFType):
    metadata_json = Storage.get_metadata(exam_id)
    return file_name in metadata_json["pdfs_done"][pdf_type.name]


def mark_pdf_done(exam_id, file_name: str, pdf_type: PDFType):
    metadata_json = Storage.get_metadata(exam_id)
    if file_name not in metadata_json["pdfs_done"][pdf_type.name]:
        metadata_json["pdfs_done"][pdf_type.name].append(file_name)
    Storage.put_file(f"{exam_id}/metadata.json", json.dumps(metadata_json))


def get_next_version(local_dir: Path, remote_dir: str):
    local_version = versioning.get_next_local_version(local_dir)
    remote_version = versioning.get_next_remote_version(remote_dir)
    return max([local_version, remote_version])


def save_answers_to_dir(
    outputdir: Path,
    results: tp.Dict[Fields, tp.Union[np.ndarray, str]],
    version: int = 0,
    image: Image = None,
    add_exam_key_sufix=False,
):
    version_str = ""
    if add_exam_key_sufix:
        version_str += f"_{get_exam_group(results)}"

    json_result = _create_output_json(results)
    outputdir.mkdir(exist_ok=True)

    if version:
        version_str += f"_{version}"

    if image is not None:
        image.save(f"{outputdir}/answers{version_str}.jpg", "JPEG")
    with open(f"{outputdir}/answers{version_str}.json", "w") as json_file:
        json.dump(json_result, json_file, sort_keys=True)
    pass


def get_exam_group(results: tp.Dict[Fields, tp.Union[np.ndarray, str]]) -> str:
    bits = [int(answer) for answer in results[Fields.exam_key][0]]
    group_id = 0
    for place, bit in enumerate(bits):
        if bit not in [0, 1]:
            return None
        group_id += bit << place
    return chr(ord("a") + group_id - 1)


def check_image(image: Image):
    fields_images = Preprocessing(np.asarray(image)).process()
    ocr_model = OCRModel(Config.paths.index_model_path)

    results = {
        f: ocr_model.inference(
            fields_images[f][0], True if f == Fields.student_id else False
        )
        for f in Fields.ocr_fields()
    }

    box_model = AnswerModel(Config.paths.answer_model_path)
    exam_key_result = box_model.inference(fields_images[Fields.exam_key])
    answer_result = box_model.inference(fields_images[Fields.answers])

    results[Fields.exam_key] = exam_key_result
    results[Fields.answers] = answer_result
    for field, result in results.items():
        logging.info(f"Detected {field.name}: {_get_readable_result(result)}")
    return results


def _create_output_json(results: tp.Dict[Fields, tp.Union[np.ndarray, str]]):
    _json = {}
    _json[Fields.exam_key.name] = [
        int(answer) for answer in results.pop(Fields.exam_key)[0]
    ]
    _json[Fields.answers.name] = {
        i + 1: [int(answer) for answer in row]
        for i, row in enumerate(results.pop(Fields.answers))
    }
    _json.update({f.name: result for f, result in results.items()})
    return _json


def _get_readable_result(result: tp.Union[np.ndarray, str]) -> str:
    if isinstance(result, str):
        return result

    output = {}
    for i, answer in enumerate(result):
        if np.any((answer == 1)):
            output[i + 1] = ", ".join(
                [chr(ord("A") + idx) for idx, val in enumerate(answer) if val]
            )
    return json.dumps(output, indent=4)
