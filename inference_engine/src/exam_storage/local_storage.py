import json
from pathlib import Path
from PIL.Image import Image

from src.config.config import Config

from src.dto.results_dto import ResultsDTO

def save_answers_to_dir(
    outputdir: Path,
    results: ResultsDTO,
    version: int = 0,
    image: Image = None,
    sufix="",
):

    json_result = results.dict()
    outputdir.mkdir(exist_ok=True)

    if version:
        sufix += f"_{version}"

    if image is not None:
        image.save(f"{outputdir}/{Config.exam_storage.result_basename}{sufix}.jpg", "JPEG")
    with open(f"{outputdir}/{Config.exam_storage.result_basename}{sufix}.json", "w") as json_file:
        json.dump(json_result, json_file, sort_keys=True)
    pass
