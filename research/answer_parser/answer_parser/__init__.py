import logging
import os

ANSWER_INTERNAL_DIR = "answers"
logger = logging.getLogger(__package__)

def save_exams_to_ground_truth(exams, output_dir):
    if os.path.isdir(output_dir) and os.listdir(path=output_dir):
            logger.warning(
                "Ground truth directory already exists. Remove it to parse answers."
            )
            return
    os.mkdir(output_dir)
    for exam in exams:
        exam.to_csv(output_dir)
