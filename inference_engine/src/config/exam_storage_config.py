from pydantic import BaseModel


class ExamStorageConfig(BaseModel):
    url: str = "http://localhost"
    port: int = 8888
    answer_key_filename: str = "answer_key"

    @property
    def full_url(self):
        return f"{self.url}:{self.port}"
