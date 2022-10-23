from pydantic import BaseModel


class ExamStorageConfig(BaseModel):
    url: str = "http://localhost"
    port: int = 8888
    exams_dir: str = "/splinter"
    answer_key_filename: str = "answer_key"
    img_extension: str = "jpg"
    default_input_dirname: str = "exams"
    default_output_dirname: str = "answers"
    exam_storage_user: str = "splinter"
    exam_storage_password: str = "1234"

    @property
    def full_answer_image_filename(self):
        return f"{self.answer_key_filename}.{self.img_extension}"

    @property
    def full_url(self):
        return f"{self.url}:{self.port}{self.exams_dir}"
