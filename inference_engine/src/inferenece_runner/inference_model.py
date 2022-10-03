from openvino.runtime import Core
from exam_solver import ExamSolver
import tensorflow as tf
import numpy as np
import keras.backend as K
import typing as tp


def macro_accuracy(y_true, y_pred):
    return K.min(K.cast(K.equal(y_true, K.round(y_pred)), dtype='float16'), axis=1)


class InferenceModel:
    def __init__(self, model_path: str = 'model\\saved_model.xml', preprocessing: tp.Callable = None,
                 postprocessing: tp.Callable = None):
        ie = Core()
        self.model = ie.compile_model(model=ie.read_model(model=model_path), device_name="CPU")
        self.output_layer = self.model.output(0)
        self.preprocessing = preprocessing or self._preprocessing
        self.postprocessing = postprocessing or self._postprocessing
        self.exam_solver = ExamSolver(None) # TODO remove init param

    @staticmethod
    def convert_model_from_h5_to_pb(input_path, output_path):
        dependencies = {
            'macro_accuracy': macro_accuracy
        }
        model = tf.keras.models.load_model(input_path, custom_objects=dependencies)
        tf.saved_model.save(model, output_path)
        return True

    def _preprocessing(self, inference_input: np.array) -> np.array:
        inference_input[inference_input < 195] = 0
        _, answer_card, box_positions = self.exam_solver.pipeline(inference_input)
        print(box_positions.shape)
        if len(inference_input.shape) < 4:
            inference_input = np.expand_dims(inference_input, 0)
        return inference_input

    def _postprocessing(self, model_output: np.array) -> tp.Union[tp.List[int], tp.List[tp.List[int]]]:
        return model_output

    def run_inference(self, input_image: np.array):
        model_input = self.preprocessing(input_image)
        model_output = self.model([model_input])[self.output_layer]
        return self.postprocessing(model_output)
