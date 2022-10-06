from openvino.runtime import Core
import numpy as np


class Model:
    def __init__(self, model_path: str):
        ie = Core()
        self.model = ie.compile_model(model=ie.read_model(model=model_path), device_name="CPU")
        self.input_layer = self.model.input(0)
        self.output_layer = self.model.output(0)

    def inference(self, _input: np.array):
        return self.model([_input])[self.output_layer]
