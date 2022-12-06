import sys
sys.path.insert(0, './object_detection')

import torch
import numpy as np
import random

from models.experimental import attempt_load
from utils.general import non_max_suppression

device = "cpu"

from handler.image_preparation_handler import ImagePreparation
from handler.plot_handler import HandlePlot


class ObjectDetection():

    def __init__(self) -> None:
        try:
            self.model = attempt_load("object_detection/model_weights/yolov7-tiny.pt", map_location=torch.device(device))
            self.model.eval()
            print("Object Detection Model loaded sucessfully")
        except:
            print("Failed loading Object Detection Model")


    def predict(image, model):
        with torch.inference_mode():
            pred = model(image[None], augment=False)[0]

        prediction = non_max_suppression(pred)[0].to(device).numpy()

        if len(prediction) > 0:
            return prediction
        else:
            return None

    def detect_objects(frame, model):
        image, original_height, original_width = ImagePreparation.prepare_image(frame)
        prediction = ObjectDetection.predict(image, model)
        if prediction is not None:
            prediction = ImagePreparation.resize_object_detection_prediction_output(prediction, original_height, original_width)
            image_with_boxes = HandlePlot.plot_bounding_boxes(prediction, frame)
            return image_with_boxes
        else:
            return frame

