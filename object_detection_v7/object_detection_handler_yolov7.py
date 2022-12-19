import sys
sys.path.insert(0, './object_detection_v7')

import torch
import numpy as np
import random

from models.experimental import attempt_load
from utils.general import non_max_suppression

device = "cuda"

from handler.image_preparation_handler import ImagePreparation
from handler.plot_handler import HandlePlot


class ObjectDetectionv7():

    def __init__(self) -> None:
        try:
            self.model = attempt_load("object_detection_v7/model_weights/yolov7-tiny.pt", map_location=torch.device(device))
            self.model.eval()
            #warmup
            image = torch.rand(640, 640, 3).permute(2, 0, 1).to(device)
            with torch.inference_mode():
                self.model(image[None], augment=False)[0]
            print("Object Detection Model loaded sucessfully")
        except:
            print("Failed loading Object Detection Model")


    def predict(self, image):
        with torch.inference_mode():
            pred = self.model(image[None], augment=False)[0]

        prediction = non_max_suppression(pred)[0].to(device)

        if len(prediction) > 0:
            return prediction
        else:
            return None

    def detect_objects(self, frame):
        image, original_height, original_width = ImagePreparation.prepare_image(frame)
        prediction = self.predict(image)
        if prediction is not None:
            prediction = ImagePreparation.resize_object_detection_prediction_output(prediction, original_height, original_width)
            image_with_boxes, person_counter = HandlePlot.plot_bounding_boxes(prediction, frame)
            return image_with_boxes, person_counter
        else:
            return frame, 0


