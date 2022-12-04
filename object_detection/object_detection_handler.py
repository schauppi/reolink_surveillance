import sys
sys.path.insert(0, './object_detection')

import torch
import numpy as np
import cv2

from models.experimental import attempt_load
from utils.general import non_max_suppression, scale_coords

#MPS working?
device = "cpu"

from pose_estimation.pose_estimation_handler import PoseEstimation


class ObjectDetection():

    def __init__(self) -> None:
        try:
            self.model = attempt_load("object_detection/model_weights/yolov7.pt", map_location=torch.device(device))
            self.model.eval()
            print("Object Detection Model loaded sucessfully")
        except:
            print("Failed loading Object Detection Model")

    def predict(image, model):
        with torch.inference_mode():
            prediction, _ = model(image)
            output_data = non_max_suppression(prediction,
                                            0.25,
                                            0.65,)

            return output_data

    def visualize_predictions(predictions, vis_image, image):
        
        for i, det in enumerate(predictions):
            print(vis_image.shape)
            vis_image = vis_image[:, :, 0]
            print(vis_image.shape)
            print(image.shape)
            det[:, :4]  = scale_coords(vis_image.shape, det[:, :4], vis_image.shape).round()
            #print(det[:, :4])
        return None


    def detect_objects(frame, model):
        image, vis_image = PoseEstimation.prepare_image_for_prediction(frame)
        preds = ObjectDetection.predict(image, model)
        out_image = ObjectDetection.visualize_predictions(preds, vis_image, image)
      
        return None