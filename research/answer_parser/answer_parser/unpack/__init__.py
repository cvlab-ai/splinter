import logging
import os
import re
import zipfile
from answer_parser import ANSWER_INTERNAL_DIR


ANSWER_ARCHIVE_RE = "answers.*\.zip"
logger = logging.getLogger(__package__)


def find_file_re(match_string: str, dir: str):
    """Find all files in the given directory that match the given regular expression.

    :param match_string: The regular expression to match the file name.
    :type match_string: str
    :param dir: The directory to search for files.
    :type dir: str
    :return: The list of files that match the given regular expression.
    :rtype: _type_
    """
    files = []
    for file in os.listdir(dir):
        if re.match(match_string, file):
            files.append(os.path.join(dir, file))
    return files


def unzip_archive(answer_archive: str, dest: str = "."):
    """Unzip the given archive into the given directory.

    :param answer_archive: The archive to unzip.
    :type answer_archive: str
    :param dest: The directory to unzip the archive into. , defaults to "."
    :type dest: str, optional
    """
    with zipfile.ZipFile(answer_archive, "r") as zip_ref:
        zip_ref.extractall(dest)


def unpack_answers(
    search_dir: str, dest: str = ".", archive_re: str = "answers.*\.zip"
):
    """Search for answer archives in the given directory and unpack them.

    :param search_dir: The directory to search for answer archives.
    :type search_dir: str
    :param dest: The directory to unpack the archives into. , defaults to "."
    :type dest: str, optional
    :param archive_re: The regular expression to match the answer archive name, defaults to 'answers.*\.zip'
    :type archive_re: str, optional
    """
    answer_dir=dest + "/" + ANSWER_INTERNAL_DIR
    if os.path.isdir(answer_dir) and os.listdir(path=answer_dir):
        logger.warning(
            "Answers directory already exists. Remove it to unpack new answers."
        )
        return

    answer_archive = find_file_re(archive_re, search_dir)
    if not answer_archive:
        print("No answer archive found")
        return
    elif len(answer_archive) > 1:
        print("More than one answer archive found:")
        print("Please select one of the following:")
        for i, archive in enumerate(answer_archive):
            print(f"({i})" + archive)
        answer_archive = answer_archive[int(input("Select archive: "))]
    else:
        answer_archive = answer_archive[0]
    logger.info(f"Unpacking {os.path.basename(answer_archive)} to {answer_dir}")
    unzip_archive(answer_archive, dest)
