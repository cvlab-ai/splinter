import json
import logging
import os

import cv2
import numpy as np

from src.preprocessing import FieldName, Field, Extractor
from .extractor import Extractor

class FieldExtractor(Extractor):

    LABEL_JSON_PATH = "./data/label.json"

    def __init__(self, field: Field):
        super().__init__(field)
        self.label_json_path = self.LABEL_JSON_PATH
        self.field_coordinates = self._load_and_map_json()

    def process(self) -> dict[FieldName, list[Field]]:
        """Extract all fields from the image using the field coordinates."""
        fields = {}
        for field_name, coordinates_list in self.field_coordinates.items():
            field_images = []
            for coordinates in coordinates_list:
                field_image = self._crop_image(self._operated_img, coordinates)
                field_images.append(Field(field_image, coordinates, field_name))
            fields[field_name] = field_images

        logging.info("Fields extracted from image.")
        return fields

    def _load_and_map_json(self) -> dict[FieldName, list[tuple[int, int, int, int]]]:
        """Load the JSON file and map field names to coordinates."""
        if not os.path.exists(self.label_json_path):
            logging.error(f"Label JSON file not found at {self.label_json_path}")
            raise FileNotFoundError(f"Label JSON file not found at {self.label_json_path}")
        with open(self.label_json_path, 'r') as file:
            json_data = json.load(file)

        field_coordinates = {}
        for field, coordinates_list in json_data.get("fields", {}).items():
            try:
                field_enum = FieldName[field.lower()]
                field_coordinates[field_enum] = [
                    (coord["x"], coord["y"], coord["width"], coord["height"]) for coord in coordinates_list
                ]
            except KeyError:
                logging.warning(f"Field '{field}' not recognized in FieldName enum.")

        logging.info(f"Field coordinates mapped from JSON.")
        return field_coordinates

    def _crop_image(self, image: np.ndarray, coordinates: tuple[int, int, int, int]) -> np.ndarray:
        """Crop the image using the provided coordinates."""
        x, y, w, h = coordinates
        cropped_image = image[y:y + h, x:x + w]
        return cropped_image



