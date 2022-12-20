import sys
sys.path.append('../')

import torch 

from models.experimental import attempt_load

device = "cpu"

def load_model():
    model = attempt_load('model_weights/yolov5n.pt', device=device)
    print("model loaded")
    return model

def export_model(model):
    input_data = torch.rand(1, 3, 640, 640)

    torch.onnx.export(model, input_data, "onnx_export/yolov5n.onnx")
    print("model exported")


if __name__ == "__main__":
    model = load_model()
    export_model(model)