import logging

import cv2

from src.controller import Controller
from src.dto import CheckExamDTO, GenerateExamKeysDTO
from src.preprocessing import Field, FieldName

logging.basicConfig(level=logging.INFO)
from src.preprocessing.extractors import FieldExtractor, BoxExtractor

# if __name__ == '__main__':
#     Controller.check_exam(CheckExamDTO.parse_obj({'exam_id': '1', 'force': 'true'}))
#     Controller.generate_exam_keys(GenerateExamKeysDTO.parse_obj({'exam_id': '1', 'force': 'true'}))

FIELD_EXTRACTOR_MAPPING = {
    FieldName.answers: BoxExtractor
}


def main():
    image = cv2.imread("./data/test.jpg")  # Assign your numpy image array here

    if image is None:
        logging.error("No image data provided.")
        return

    try:
        fields = FieldExtractor(Field(image)).process()
        _map = FIELD_EXTRACTOR_MAPPING
        # result = [(name, _map[name](field).process()) for name, field in fields.items() if name in _map]
        # apply the extractor function for each item in 'fields' if the field name is in the mapping
        result = []
        for name, field in fields.items():
           func = _map[name]
           for item in field:
               result.append((name, func(item).process()))

        print(result)
        # Now 'answers' is a list of numpy arrays representing each answer option
        # You can proceed to process or save them as needed
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

    # def process(self) -> tp.Tuple[tp.Dict[FieldName, tp.List[Field]], np.ndarray]:
    #     self._exam_copy = rotate_exam(self._exam_copy)
    #     try:
    #         fields = FieldExtractor(Field(self._exam_copy)).process()
    #         _map = Preprocessing.FIELD_EXTRACTOR_MAPPING
    #         result = [(name, _map[name](field).process()) for name, field in fields if name in _map]
    #         result = self.group_by_field(result)
    #     except (IndexError, ValueError, cv2.error) as e:
    #         logging.exception(e)
    #         raise PreprocessingError(e)
    #     return result, self._exam_copy