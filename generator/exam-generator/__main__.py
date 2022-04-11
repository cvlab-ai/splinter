from . import ExamGenerator, GeneratorConfig


def main():
    exam_generator = ExamGenerator(GeneratorConfig())
    exam_generator.generate()


if __name__ == '__main__':
    main()
