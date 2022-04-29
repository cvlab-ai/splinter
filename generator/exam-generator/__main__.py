import os
import pathlib
import typing as tp
import shutil

from . import ExamGenerator, GeneratorConfig
from .instruction_generator import generate_exam_instruction
from .generator_args import GeneratorArgs

exams_names = []


def check_unique_names(name: str):
    if name in exams_names:
        return False
    exams_names.append(name)
    return True


def zip_files(zip_file: str, filenames: tp.List[str]):
    with zipfile.ZipFile(zip_file, "w") as zipF:
        for file in filenames:
            zipF.write(file, compress_type=zipfile.ZIP_DEFLATED)
            os.remove(file)


def generate_package(
    name: str, config: GeneratorConfig, metadata_name: str = "metadata"
):
    exam_generator = ExamGenerator(config)
    exam_generator.generate(name)
    config.export(f"{metadata_name}.json")
    generate_exam_instruction(config.number_of_answers, f"{name}.txt")


def generate_set(number_of_exams: int, set_name: str, metadata_dir: str):
    for _ in range(number_of_exams):
        config = GeneratorConfig.random()
        while not check_unique_names(str(config.exam_id)):
            config = GeneratorConfig.random()

        exam_dir = pathlib.Path(f"{set_name}/{config.exam_id}")
        exam_dir.mkdir(parents=True)

        base_filename = str(config.exam_id)

        name = f"{str(exam_dir)}/{base_filename}"
        metadata_name = f"{str(metadata_dir)}/{base_filename}"
        generate_package(name, config, metadata_name)


def main():
    args = GeneratorArgs().parse_args()

    if args.test:
        config = GeneratorConfig.random()
        generate_package("exam", config)
        exit()

    dest_dir = pathlib.Path(args.destdir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir = pathlib.Path(f"{args.destdir}/metadata")
    metadata_dir.mkdir(parents=True, exist_ok=True)

    for i in range(args.sets):
        set_dir = pathlib.Path(f"{dest_dir}/set{i}")
        set_dir.mkdir(parents=True)
        generate_set(args.number, str(set_dir), str(metadata_dir))

        if args.zip:
            shutil.make_archive(f"{set_dir}", 'zip', f"{set_dir}")
            # zip_files(f"{set_dir}.zip", f"{dest_dir}")


if __name__ == "__main__":
    main()
