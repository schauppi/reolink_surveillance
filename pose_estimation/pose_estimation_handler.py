import sys
sys.path.insert(0, './pose_estimation')

import torch
import numpy as np

from models.experimental import attempt_load

from utils.general import non_max_suppression_kpt
from utils.plots import output_to_keypoint, colors

from handler.image_preparation_handler import ImagePreparation
from handler.plot_handler import HandlePlot

#MPS not working for YOLOv7
device = "cpu"

class PoseEstimation():

    def __init__(self) -> None:
        try:
            self.model = attempt_load("pose_estimation/model_weights/yolov7-w6-pose.pt", map_location=torch.device(device))
            self.model.eval()
            print("Pose Estimation Model loaded sucessfully")
        except:
            print("Failed loading Pose Estimation Model")

    def predict(image, model):
        with torch.inference_mode():
            pred = model(image[None], augment=False)[0]

        prediction = non_max_suppression_kpt(pred,
        0.25, 0.65, nc=model.yaml['nc'], nkpt=model.yaml['nkpt'], kpt_label=True)

        prediction = output_to_keypoint(prediction)
        if len(prediction) > 0:
            prediction = prediction[:, 7:]
            return prediction
        else:
            return None


    def detect_poses(frame, model):
        image, original_height, original_width = image, original_height, original_width = ImagePreparation.prepare_image(frame)
        prediction = PoseEstimation.predict(image, model)
        if prediction is not None:
            prediction = ImagePreparation.resize_pose_estimation_prediction_output(prediction, original_height, original_width)
            image_with_poses = HandlePlot.plot_pose(prediction)
            return image_with_poses
        else:
            return frame
