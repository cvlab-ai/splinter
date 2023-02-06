#!/usr/bin/env python3

import sys
from pathlib import Path
import zlib


STORAGE_BASEDIR = Path("/www/data/splinter/internal/")
SPLINTER_BASEDIR = Path(STORAGE_BASEDIR / "splinter-data/")
ZIP_BASEDIR = Path(SPLINTER_BASEDIR / "zip/")
exam_path = Path(SPLINTER_BASEDIR / Path(sys.argv[1]).name)


def crc(fileName):
    prev = 0
    for eachLine in open(fileName, "rb"):
        prev = zlib.crc32(eachLine, prev)
    return "%X" % (prev & 0xFFFFFFFF)


def list_files(dir: Path):
    files = []
    for file in dir.iterdir():
        if file.is_dir():
            files.extend(list_files(file))
        else:
            file_crc = crc(file)
            size = file.stat().st_size
            input_filename = file.relative_to(STORAGE_BASEDIR)
            output_filename = file.relative_to(exam_path)
            files.append(f"{file_crc} {size} /{input_filename} /{output_filename}")
    return files


print(f"Compressing exam: {exam_path}")
if not exam_path.is_dir():
    sys.exit()

ZIP_BASEDIR.mkdir(exist_ok=True)

with open(ZIP_BASEDIR / exam_path.name, "w") as zip:
    zip.writelines("\n".join(list_files(exam_path)) + "\n")
