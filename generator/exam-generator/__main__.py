from . import ExamGenerator, GeneratorConfig
from .instruction_generator import generate_exam_instruction


def main():
    config = GeneratorConfig.random()
    exam_generator = ExamGenerator(config)
    exam_generator.generate()
    generate_exam_instruction(config.number_of_answers, "exam.txt")


if __name__ == "__main__":
    main()
