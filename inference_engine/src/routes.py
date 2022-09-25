import logging

from flask import Blueprint, request

from .dto import CheckExamDTO, CheckExamsDTO, GenerateExamKeyDTO
from .controller import Controller

routes = Blueprint('routes', __name__)


@routes.before_request
def log_request():
    logging.info(f"--- New request approach: {request.method} {request.path} {request.json}")


@routes.route("check-exam", methods=['POST'])
def check_exam():
    Controller.check_exam(CheckExamDTO.from_dict(request.json))
    return "Success!"


@routes.route("check-exams", methods=['POST'])
def check_exam():
    Controller.check_exams(CheckExamsDTO.from_dict(request.json))
    return "Success!"


@routes.route("generate-exam-key", methods=['POST'])
def generate_exam_key():
    Controller.generate_exam_key(GenerateExamKeyDTO.from_dict(request.json))
    return "Success!"
