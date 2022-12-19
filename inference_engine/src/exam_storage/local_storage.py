import json
from pathlib import Path

import numpy as np
from PIL import Image

from src.config.config import Config
from src.dto.results_dto import ResultsDTO


def save_answers_to_dir(
    outputdir: Path,
    results: ResultsDTO,
    version: int = 0,
    image: Image.Image = None,
    debug_image: np.ndarray = None,
    sufix="",
):

    json_result = results.dict()
    outputdir.mkdir(exist_ok=True)

    if version:
        sufix += f"_{version}"

    if image is not None:
        image.save(f"{outputdir}/{Config.exam_storage.result_basename}{sufix}.jpg", "JPEG")
    if debug_image is not None:
        debug_image = Image.fromarray(debug_image)
        debug_filename = f"{Config.exam_storage.result_basename}{sufix}{Config.exam_storage.debug_image_sufix}.jpg"
        debug_image.save(f"{outputdir}/{debug_filename}", "JPEG")
    with open(f"{outputdir}/{Config.exam_storage.result_basename}{sufix}.json", "w") as json_file:
        json.dump(json_result, json_file, sort_keys=True, indent=4)
    pass
