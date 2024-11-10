import logging
import os

import cv2
import numpy as np
from PIL import Image

from src.preprocessing import Field, FieldName

logging.basicConfig(level=logging.INFO)
from src.preprocessing.extractors import FieldExtractor, BoxExtractor, TextExtractor, GroupExtractor

# if __name__ == '__main__':
#     Controller.check_exam(CheckExamDTO.parse_obj({'exam_id': '1', 'force': 'true'}))
#     Controller.generate_exam_keys(GenerateExamKeysDTO.parse_obj({'exam_id': '1', 'force': 'true'}))

FIELD_EXTRACTOR_MAPPING = {
    FieldName.answers: BoxExtractor,
    FieldName.exam_key: GroupExtractor,
    # FieldName.student_name: TextExtractor,
    # FieldName.exam_title: TextExtractor,
    # FieldName.date: TextExtractor
}

OUTPUT_DIR = "./data/output"

def show_image(image: np.ndarray, title=""):
    pil_image = Image.fromarray(image)
    pil_image.show(title=title)

def save_image(image: np.ndarray, path: str):
    cv2.imwrite(path, image)

def merge_answer_rows(answer_array: np.ndarray) -> list[np.ndarray]:
    merged_rows = [np.concatenate(row, axis=1) for row in answer_array]
    return merged_rows


def save_answers(answers: list[Field]):
    answers_merged_output_dir = f"{OUTPUT_DIR}/answers_merged"
    os.makedirs(answers_merged_output_dir, exist_ok=True)
    for i, answer in enumerate(answers):
        rows = merge_answer_rows(answer.img)
        for j, row in enumerate(rows):
            save_image(row, os.path.join(answers_merged_output_dir, f"answer_{i}_row_{j}.jpg"))

    answers_not_merged_output_dir = f"{OUTPUT_DIR}/answers_not_merged"
    os.makedirs(answers_not_merged_output_dir, exist_ok=True)
    for i, answer in enumerate(answers):
        answer_box_output_dir = f"{answers_not_merged_output_dir}/answer_{i}"
        os.makedirs(answer_box_output_dir, exist_ok=True)
        img = answer.img
        number_of_answer_rows = img.shape[0]
        number_of_answer_options = img.shape[1]
        for row in range(number_of_answer_rows):
            answer_row_output_dir = f"{answer_box_output_dir}/row_{row}"
            os.makedirs(answer_row_output_dir, exist_ok=True)
            for col in range(number_of_answer_options):
                save_image(img[row][col], os.path.join(answer_row_output_dir, f"col_{col}.jpg"))

def save_groups(groups: list[Field]):
    groups_output_dir_merged = f"{OUTPUT_DIR}/groups_merged"
    os.makedirs(groups_output_dir_merged, exist_ok=True)
    for i, group in enumerate(groups):
        rows = merge_answer_rows(group.img)
        for j, row in enumerate(rows):
            save_image(row, os.path.join(groups_output_dir_merged, f"group_{i}_row_{j}.jpg"))

    groups_output_dir_not_merged = f"{OUTPUT_DIR}/groups_not_merged"
    os.makedirs(groups_output_dir_not_merged, exist_ok=True)
    for i, group in enumerate(groups):
        group_box_output_dir = f"{groups_output_dir_not_merged}/group_{i}"
        os.makedirs(group_box_output_dir, exist_ok=True)
        img = group.img
        number_of_group_rows = img.shape[0]
        number_of_group_options = img.shape[1]
        for row in range(number_of_group_rows):
            group_row_output_dir = f"{group_box_output_dir}/row_{row}"
            os.makedirs(group_row_output_dir, exist_ok=True)
            for col in range(number_of_group_options):
                save_image(img[row][col], os.path.join(group_row_output_dir, f"col_{col}.jpg"))


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
        include_only = [FieldName.answers, FieldName.exam_key]
        fields = {name: field for name, field in fields.items() if name in include_only}

        for name, field in fields.items():
            logging.info(f"Processing field: {name}")
            func = _map[name]
            for item in field:
                result.append((name, func(item).process()))

        # filter only answers field from result
        # answers = [answer for name, answer in result if name == FieldName.answers]
        # save_answers(answers)
        groups = [group for name, group in result if name == FieldName.exam_key]
        save_groups(groups)
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
