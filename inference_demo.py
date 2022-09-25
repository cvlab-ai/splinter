from inference_engine.src.inferenece_runner.inference_model import InferenceModel
from research.marked_answer_card_generator import MarkedAnswerCardGenerator
import numpy as np


# mo --saved_model_dir src\inferenece_runner\model\CNN_answer_full.pb
marked_answer_card_generator = MarkedAnswerCardGenerator("research/data/exams/image--000.jpg", (290, 60))
row_generator = marked_answer_card_generator.row_generator()
row_image, label = next(row_generator)
model = InferenceModel("inference_engine\\src\\inferenece_runner\\model\\saved_model.xml")
print(model.run_inference(row_image), label)
