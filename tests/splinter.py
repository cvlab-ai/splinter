import os
import docker
import requests
import webdav3.client
import webdav3.exceptions


class DockerService():
    def __init__(self, service_name) -> None:
        client = docker.DockerClient()
        network = 'splinter_default'
        container = client.containers.get(service_name)
        self.ip_addr = container.attrs["NetworkSettings"]["Networks"][network]["IPAddress"]
        self.port = 8000

    @property
    def url(self):
        return f'http://{self.ip_addr}:{self.port}'

    def send_request(self, path, method='POST', json=None):
        r = requests.request(method, url=f'{self.url}/{path}', json=json)
        return r


class InfEngine(DockerService):
    def __init__(self) -> None:
        super().__init__("splinter_splinter-inference-engine_1")

    def check_exam(self, exam_id, force=False):
        body ={"exam_id": exam_id, "force": force}
        r = self.send_request('check-exam', json=body)
        r.raise_for_status()

    def check_answers_pdf(self, exam_id, file_name, force=False):
        body ={"exam_id": exam_id, "file_name": file_name, "force": force}
        r = self.send_request('check-answers-pdf', json=body)
        r.raise_for_status()

    def generate_exam_keys(self, exam_id, file_name=None, force=False):
        body ={"exam_id": exam_id, "file_name": file_name, "force": force}
        r = self.send_request('generate-exam-keys', json=body)
        r.raise_for_status()


class ExamStorage(DockerService):
    def __init__(self) -> None:
        super().__init__("splinter_splinter-exam-storage_1")
        self.port = 80
        splinter_options = {
            'webdav_hostname': self.url + '/splinter',
            'webdav_login': os.getenv("EX_STORE_SPLINTER_USER"),
            'webdav_password': os.getenv("EX_STORE_SPLINTER_PASS")
        }
        self.splinter = webdav3.client.Client(splinter_options)

    def clean_splinter(self):
        try:
            self.splinter.clean("/")
        except webdav3.exceptions.WebDavException:
            pass
