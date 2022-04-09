import logging
from . import ExamGenerator, GeneratorConfig
from .logger import logger
from . import config


def main():
    print("MAIN")
    exam_generator = ExamGenerator(GeneratorConfig())
    exam_generator.generate()


if __name__ == '__main__':
    main()
