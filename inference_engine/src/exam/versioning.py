from pathlib import Path
from src.storage import Storage

def get_next_remote_version(remote_dir):
    dir_content = Storage._get_dir(remote_dir)
    if dir_content is None:
        return 0
    version_candidates = _filter_versioned_files([row['name'] for row in dir_content])
    return _find_next_file_version(version_candidates)

def get_next_local_version(dir: Path):
    if not dir.exists():
        return 0
    version_candidates = _filter_versioned_files(
        [file.name for file in dir.iterdir() if file.is_file()]
    )
    return _find_next_file_version(version_candidates)

def _filter_versioned_files(files, base_filename='answers', ext='json'):
    names = []
    for filename in files:
        name, ext = filename.split('.', 1)
        if ext == 'json' and name.startswith(base_filename):
            names.append(name)
    return names


def _find_next_file_version(files):
    if len(files) == 0:
        return 0
    latest_name = max(files)
    version = latest_name.split('_')[-1]
    if version.isnumeric():
        return int(version) + 1
    # some files exist but without version,
    # that means next one should be versioned
    return 1
