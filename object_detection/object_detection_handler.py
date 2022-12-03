import sys
sys.path.insert(0, './object_detection')

import torch
import numpy as np

from models.experimental import attempt_load

#MPS working?
device = "cpu"


class ObjectDetection():

    def __init__(self) -> None:
        try:
            self.model = attempt_load("object_detection/model_weights/yolov7.pt", map_location=torch.device(device))
            self.model.eval()
            print("Object Detection Model loaded sucessfully")
        except:
            print("Failed loading Object Detection Model")



    def detect_objects(frame, model):
   
        return None