from pathlib import Path
from src.config.config import Config
from src.exam_storage import remote_storage
import typing as tp


def get_next_remote_version(remote_dir, sufix=""):
    return get_latest_remote_version(remote_dir, sufix="") + 1


def get_next_local_version(dir: Path, sufix=""):
    if not dir.exists():
        return 0
    version_candidates = _filter_versioned_files(
        [file.name for file in dir.iterdir() if file.is_file()],
        base_filename=Config.exam_storage.result_basename + sufix,
    )
    return _find_next_file_version(version_candidates)


def _filter_versioned_files(files, base_filename="answers", ext="json"):
    names = []
    for filename in files:
        name, ext = filename.split(".", 1)
        if ext == "json" and name.startswith(base_filename):
            names.append(name)
    return names


def _find_next_file_version(files):
    if len(files) == 0:
        return 0
    latest_name = max(files)
    version = latest_name.split("_")[-1]
    if version.isnumeric():
        return int(version) + 1
    # some files exist but without version,
    # that means next one should be versioned
    return 1


def examkey2group(exam_key: tp.List[int]) -> str:
    try:
        group_id = exam_key.index(1)
    except:
        return ""
    return chr(ord("a") + group_id)


def get_next_version(local_dir: Path, remote_dir: str, sufix="") -> int:
    local_version = get_next_local_version(local_dir, sufix)
    remote_version = get_next_remote_version(remote_dir, sufix)
    return max([local_version, remote_version])


def get_latest_remote_version(remote_dir: str, sufix="") -> int:
    dir_content = remote_storage.get_dir(remote_dir)
    if dir_content is None:
        return 0
    version_candidates = _filter_versioned_files(
        [row["name"] for row in dir_content],
        base_filename=Config.exam_storage.result_basename + sufix,
    )
    return _find_latest_file_version(version_candidates)


def _find_latest_file_version(files: tp.List[str]) -> int:
    if len(files) == 0:
        return 0
    latest_name = max(files)
    version = latest_name.split("_")[-1]
    if version.isnumeric():
        return int(version)
    # some files exist but without version,
    # that means it's version is 0
    return 0

def v2s(version: int) -> str:
    suffix = ""
    if version:
        suffix = f"_{version}"
    return suffix

