import sys
sys.path.insert(0, './object_detection')

import torch
import numpy as np
import cv2
import random

from models.experimental import attempt_load
from utils.general import non_max_suppression, scale_coords
from utils.plots import plot_one_box

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

    def visualize_predictions(predictions, vis_image, model, frame):
        colors = [[random.randint(0, 255) for _ in range(3)] for _ in model.names]
        with torch.inference_mode():
        
            for i, det in enumerate(predictions):
                vis_image = vis_image[:, :, 0]
                if len(det):
                    det[:, :4]  = scale_coords(vis_image.shape, det[:, :4], vis_image.shape).round()

                    for *xyxy, conf, cls in reversed(det):
                        """
                        Get correct labels
                        """
                        plot_one_box(xyxy, frame, label="test", color=colors[int(cls)], line_thickness=1)
        return frame
                


    def detect_objects(frame, model):
        image, vis_image = PoseEstimation.prepare_image_for_prediction(frame)
        preds = ObjectDetection.predict(image, model)
        out_image = ObjectDetection.visualize_predictions(preds, vis_image, model, frame)
      
        return out_image