import os
import pathlib
import typing as tp
import zipfile

from . import ExamGenerator, GeneratorConfig
from .instruction_generator import generate_exam_instruction


def zip_files(zip_file: str, filenames: tp.List[str]):
    with zipfile.ZipFile(zip_file, 'w') as zipF:
        for file in filenames:
            zipF.write(file, compress_type=zipfile.ZIP_DEFLATED)
            os.remove(file)



def main():
    config = GeneratorConfig.random()
    exam_generator = ExamGenerator(config)

    base_filename = str(config.exam_id)
    exam_generator.generate(base_filename)
    config.export(f"exams/{base_filename}.json")
    generate_exam_instruction(config.number_of_answers, f"{base_filename}.txt")

    pathlib.Path(f"exams").mkdir(parents=True, exist_ok=True)
    zip_files(f"exams/{base_filename}.zip", [f"{base_filename}.pdf", f"{base_filename}.txt"])

if __name__ == "__main__":
    main()
