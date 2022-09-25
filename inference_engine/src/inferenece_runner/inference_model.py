from openvino.runtime import Core
import tensorflow as tf
import numpy as np
import keras.backend as K


def macro_accuracy(y_true, y_pred):
    return K.min(K.cast(K.equal(y_true, K.round(y_pred)), dtype='float16'), axis=1)


class InferenceModel:
    def __init__(self, model_path: str = 'model\\saved_model.xml'):
        ie = Core()
        self.model = ie.compile_model(model=ie.read_model(model=model_path), device_name="CPU")
        self.output_layer = self.model.output(0)

    @staticmethod
    def convert_model_from_h5_to_pb(input_path, output_path):
        dependencies = {
            'macro_accuracy': macro_accuracy
        }
        model = tf.keras.models.load_model(input_path, custom_objects=dependencies)
        tf.saved_model.save(model, output_path)
        return True

    def run_inference(self, input_value: np.array):
        input_value = np.expand_dims(input_value, 0)
        return self.model([input_value])[self.output_layer]
