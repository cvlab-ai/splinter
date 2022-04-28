import os
import pathlib
import typing as tp
import zipfile

from . import ExamGenerator, GeneratorConfig
from .instruction_generator import generate_exam_instruction
from .generator_args import GeneratorArgs


def zip_files(zip_file: str, filenames: tp.List[str]):
    with zipfile.ZipFile(zip_file, "w") as zipF:
        for file in filenames:
            zipF.write(file, compress_type=zipfile.ZIP_DEFLATED)
            os.remove(file)


def generate_package(name: str, config: GeneratorConfig):
    exam_generator = ExamGenerator(config)
    exam_generator.generate(name)
    config.export(f"{name}.json")
    generate_exam_instruction(config.number_of_answers, f"{name}.txt")


def main():
    args = GeneratorArgs().parse_args()
    # Make sure output directory exists
    pathlib.Path(args.destdir).mkdir(parents=True, exist_ok=True)

    for _ in range(args.number):
        config = GeneratorConfig.random()
        base_filename = f"{args.destdir}/{str(config.exam_id)}"
        if args.test:
            base_filename = f"{args.destdir}/exam"

        generate_package(base_filename, config)
        if args.zip:
            zip_files(
                f"{base_filename}.zip",
                [
                    f"{base_filename}.pdf",
                    f"{base_filename}.txt",
                ],
            )


if __name__ == "__main__":
    main()
