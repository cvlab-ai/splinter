import typing as tp
import logging

import numpy as np
import json
import tempfile
import pdf2image
from pathlib import Path
from PIL.Image import Image

from src.config import Config
from .storage import Storage
from .preprocessing import Preprocessing, Fields
from .model import AnswerModel, OCRModel
from .dto import CheckPdfDTO, CheckExamDTO, GenerateExamKeysDTO

class Controller:
    @staticmethod
    def check_pdf(request: CheckPdfDTO):
        input_dir = Controller._add_io_path(request.exam_id, Config.exam_storage.default_input_dirname)
        metadata_json = Storage.get_file(f"{request.exam_id}/metadata.json")
        if metadata_json is None:
            metadata_json = {'pdfs_done': []}
        else:
            metadata_json = metadata_json.json()

        if 'pdfs_done' not in metadata_json:
            metadata_json['pdfs_done'] = []
        else:
            if request.file_name in metadata_json['pdfs_done'] and not request.force:
                logging.info(f"PDF {request.file_name} already checked, skipping.")
                return

        with tempfile.TemporaryDirectory() as tmpdirname:
            images = Controller.unpack_pdf(f"{input_dir}/{request.file_name}")
            for image in images:
                index_result, answer_result = Controller.check_image(image)
                json_result = Controller._create_output_json(answer_result, index_result)
                student_dir = Path(f"{tmpdirname}/{index_result}")
                version_str = ''
                if student_dir.exists():
                    version = Controller._get_next_local_version(student_dir)
                else:
                    student_dir.mkdir()
                    version = Storage.next_answer_version(request.exam_id, index_result)
                if version:
                    version_str = f'_{version}'
                image.save(f"{student_dir}/answers{version_str}.jpg", "JPEG")
                with open(f"{student_dir}/answers{version_str}.json", "w") as json_file:
                    json.dump(json_result, json_file)
            tmpdir = Path(tmpdirname)
            for student_dir in tmpdir.iterdir():
                Storage.push_student_dir(request.exam_id, student_dir)
            if request.file_name not in metadata_json['pdfs_done']:
                metadata_json['pdfs_done'].append(request.file_name)
            Storage.put_file(f'{request.exam_id}/metadata.json', json.dumps(metadata_json))

    @staticmethod
    def check_exam(request: CheckExamDTO):
        logging.info(f"Checking exam: {request.exam_id}")
        for file_name in Storage.get_pdfs_names(request.exam_id):
            logging.info(f"Checking pdf: {file_name}")
            Controller.check_pdf(CheckPdfDTO.parse_obj({'exam_id': request.exam_id, 'file_name' : file_name, 'force': request.force}))

    @staticmethod
    def generate_exam_keys(request: GenerateExamKeysDTO):
        Controller._mark_detection(request.exam_path, f'{Config.exam_storage.full_answer_image_filename}',
                                   request.exam_path)

    @staticmethod
    def check_image(image: Image):
        answer_input, index_input = Preprocessing().process(np.asarray(image))
        index_result = IndexModel(Config.paths.index_model_path).inference(index_input)
        logging.info(f"Detected index: {index_result}")
        answer_result = AnswerModel(Config.paths.answer_model_path).inference(answer_input)
        logging.info(f"Detected answers: {Controller._get_readable_answers(answer_result)}")
        return index_result, answer_result

    @staticmethod
    def _get_next_local_version(student_dir: Path):
            if not student_dir.exists():
                return 0
            version_candidates = Storage._filter_versioned_files([file.name for file in student_dir.iterdir()])
            return Storage._find_next_file_version(version_candidates)


    @staticmethod
    def _add_io_path(exam_path: str, io_path: str):
        return f"{exam_path}/{io_path}/"

    @staticmethod
    def unpack_pdf(file_path: str):
        return pdf2image.convert_from_bytes(Storage.get_file(file_path).content)


    @staticmethod
    def _mark_detection(file_path: str, file_name: str, output_path: str):
        image = Storage.get_exam_image(file_path, file_name)
        fields_images = Preprocessing(image).process()
        ocr_model = OCRModel(Config.paths.index_model_path)

        ocr_results = {f: ocr_model.inference(fields_images[f][0], True if f == Fields.student_id else False)
                       for f in Fields.ocr_fields()}
        for field, result in ocr_results.items():
            logging.info(f"Detected {field.name}: {result}")

        box_model = AnswerModel(Config.paths.answer_model_path)

        exam_key_result = box_model.inference(fields_images[Fields.exam_key])
        logging.info(f"Detected exam key: {Controller._get_readable_answers(exam_key_result)}")

        answer_result = box_model.inference(fields_images[Fields.answer_column])
        logging.info(f"Detected answers: {Controller._get_readable_answers(answer_result)}")

        json_result = Controller._create_output_json(answer_result, ocr_results)
        Storage.set_exam_answer_json(output_path, file_name, json_result)

    @staticmethod
    def _create_output_json(answers: np.ndarray, ocr_results: tp.Dict[Fields, str]):
        _json = {f.name: result for f, result in ocr_results.items()}
        _json["answers"] = {i + 1: [int(answer) for answer in row] for i, row in enumerate(answers)}
        return _json

    @staticmethod
    def _get_readable_answers(answers: np.ndarray) -> str:
        return json.dumps({i + 1: ', '.join(
            [chr(ord('A') + idx) for idx, val in enumerate(answer) if val]
        ) for i, answer in enumerate(answers) if np.any((answer == 1))}, indent=4)
