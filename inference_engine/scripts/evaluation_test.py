import json
import os
from pathlib import Path

from PIL import Image
from tqdm import tqdm

from src.controller import _check_image


def collect_data_paths(root_dir):
    root_dir = Path(root_dir)
    data = []

    directories = [p for p in root_dir.rglob('*') if p.is_dir()]
    for dirpath in tqdm(directories, desc='Processing directories'):
        required_files = {"log.txt", "orig.png"}
        files_in_dir = {file.name for file in dirpath.iterdir() if file.is_file()}

        if required_files.issubset(files_in_dir):
            log_file = dirpath / 'log.txt'
            img_file = dirpath / 'orig.png'

            data.append({
                "file_name": img_file.name,
                "log_path": str(log_file),
                "img_path": str(img_file),
                "dir_path": str(dirpath)
            })

    return data


def save_metadata_to_catalog(results, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for idx, result in enumerate(results):
        result_file = output_dir / f"result_{idx + 1}.json"
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=4)

        print(f"Saved result to {result_file}")


if __name__ == "__main__":
    root_dir = "./data/exams-anon"
    output_dir = "./data/results"
    os.makedirs(output_dir, exist_ok=True)

    data = collect_data_paths(root_dir)
    print(f"Collected data paths for {len(data)} directories.")

    errors = []
    results = []
    for entry in tqdm(data, desc='Checking images'):
        _, log_path, img_path, dir_path = entry.values()
        image = Image.open(img_path)
        try:
            result, _ = _check_image(image)
            entry['inference_engine_result'] = result.dict()
            results.append(entry)
        except Exception as e:
            print(f"Error while checking image {img_path}: {e}")
            errors.append(f"Error while checking image {img_path}: {e}")
            continue

    save_metadata_to_catalog(results, output_dir)

    if errors:
        with open('data/errors.txt', 'w') as f:
            for error in errors:
                f.write(f"{error}\n")

        print(f"Errors saved to errors.txt")
