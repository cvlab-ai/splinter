import json
import logging
import os

from src.config import Config
from src.preprocessing import FieldName, Field
from src.utils import ImageProcessor
from .extractor import Extractor


class FieldExtractor(Extractor):

    def __init__(self, field: Field):
        super().__init__(field)
        self.field_coordinates_path = Config.paths.field_coordinates_path
        self.coordinates_map = self._load_coordinates_map()

    def process(self) -> dict[FieldName, list[Field]]:
        """Extracts defined regions for each field from the image.

        Returns:
            dict[FieldName, list[Field]]: A mapping of each field name to a list of Field objects,
            each representing a specific region in the image where that field is located.
        """
        field_regions = {}
        for field_name, coordinates_list in self.coordinates_map.items():
            field_images = []
            for coordinates in coordinates_list:
                field_image = ImageProcessor.crop_image(self._operated_img, coordinates)
                field_images.append(Field(field_image, coordinates, field_name))
            field_regions[field_name] = field_images

        logging.info("Fields extracted from image.")
        return field_regions

    def _load_coordinates_map(self) -> dict[FieldName, list[tuple[int, int, int, int]]]:
        if not os.path.exists(self.field_coordinates_path):
            logging.error(f"Label JSON file not found at {self.field_coordinates_path}")
            raise FileNotFoundError(f"Label JSON file not found at {self.field_coordinates_path}")

        with open(self.field_coordinates_path, 'r') as file:
            json_data = json.load(file)

        field_coordinates = {}
        for field, coordinates_list in json_data.get("fields", {}).items():
            try:
                field_enum = FieldName[field.upper()]
                field_coordinates[field_enum] = [
                    (coord["x"], coord["y"], coord["width"], coord["height"]) for coord in coordinates_list
                ]
            except KeyError:
                logging.warning(f"Field '{field}' not recognized in FieldName enum.")

        logging.info(f"Field coordinates mapped from JSON.")
        return field_coordinates
