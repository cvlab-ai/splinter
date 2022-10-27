import json
from src.config.config import Config
from src.exam_storage import remote_storage
from src.exam_storage.pdf_type import PDFType
import enum


class Metadata(enum.Enum):
    pdfs_done = 1


def check_pdf_processed(exam_id, file_name, pdf_type: PDFType):
    metadata_json = get_metadata(exam_id)
    return file_name in metadata_json[Metadata.pdfs_done.name][pdf_type.name]


def mark_pdf_done(exam_id, file_name: str, pdf_type: PDFType):
    metadata_json = get_metadata(exam_id)
    if file_name not in metadata_json[Metadata.pdfs_done.name][pdf_type.name]:
        metadata_json[Metadata.pdfs_done.name][pdf_type.name].append(file_name)
    remote_storage.put_file(
        f"{exam_id}/{Config.exam_storage.metadata_filename}", json.dumps(metadata_json)
    )


def get_metadata(exam_id: int):
    metadata_json = remote_storage.get_file(
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
