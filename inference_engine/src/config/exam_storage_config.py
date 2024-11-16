import os
from pydantic import BaseModel


class ExamStorageConfig(BaseModel):
    url: str = "http://localhost"
    port: int = 8888
    exams_dir: str = "/splinter"
    answer_keys_dir: str = "answers_keys"
    answer_key_filename: str = "answer_key"
    pdf_extension: str = "pdf"
    allowed_image_extensions: tuple[str] = (".png", ".jpg", ".jpeg", ".tif", ".tiff")
    allowed_extensions: tuple[str] = (pdf_extension, *allowed_image_extensions)
    default_input_dirname: str = "pdfs"
    default_output_dirname: str = "students"
    exam_storage_user: str = os.environ.get("EX_STORE_SPLINTER_USER")
    exam_storage_password: str = os.environ.get("EX_STORE_SPLINTER_PASS")
    metadata_filename: str = "metadata.json"
    result_basename: str = "answers"
    debug_image_sufix: str = "_debug"

    @property
    def full_url(self):
        return f"{self.url}:{self.port}{self.exams_dir}"
