import sys
sys.path.append('../')

import torch 

from models.experimental import attempt_load

device = "cpu"

model = attempt_load('model_weights/yolov5n.pt', device=device)

input_data = torch.rand(1, 3, 640, 640)

torch.onnx.export(model, input_data, "yolov5n.onnx")