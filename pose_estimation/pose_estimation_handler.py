import sys
sys.path.insert(0, './pose_estimation')

import torch
from torchvision import transforms
import cv2
import numpy as np

from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import non_max_suppression_kpt
from utils.plots import output_to_keypoint, plot_one_box_kpt, colors

device = "cpu"

class PoseEstimation():

    def __init__(self) -> None:
        try:
            self.model = attempt_load("pose_estimation/model_weights/yolov7-w6-pose.pt", map_location=torch.device(device))
            self.model.eval()
            print("Pose Estimation Model loaded sucessfully")
        except:
            print("Failed loading Pose Estimation Model")

    def prepare_image_for_prediction(frame):
        orig_image = frame
        frame_width = frame.shape[1]
        image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
        image = letterbox(image, (frame_width), stride=64, auto=True)[0]
        image = transforms.ToTensor()(image)
        image = torch.tensor(np.array([image.numpy()]))
        image = image.to(device)

        vis_image = image[0].permute(1, 2, 0) * 255
        vis_image = vis_image.cpu().numpy().astype(np.uint8)
        vis_image = cv2.cvtColor(vis_image, cv2.COLOR_RGB2BGR)

        return image, vis_image

    def predict(image, model):
        with torch.inference_mode():
            prediction, _ = model(image)
            output_data = non_max_suppression_kpt(prediction, 
                                            0.25, #conf. Tresh
                                            0.65, # IoU Tresh
                                            nc=model.yaml['nc'], #classes
                                            nkpt=model.yaml['nkpt'], #num KP
                                            kpt_label=True)

            output = output_to_keypoint(output_data)
            return output_data

    def visualize_predictions(predictions, vis_image):

        for i, pose in enumerate(predictions):

            if len(predictions) == 0:
                print("No detections")
                return None

            else:
                for det_index, (*xyxy, conf, cls) in enumerate(reversed(pose[:,:6])):
                    c = int(cls)
                    kpts = pose[det_index, 6:]
                    print(kpts)
                    plot_one_box_kpt(xyxy, vis_image, label=None, color=colors(c, True), 
                                        line_thickness=3,kpt_label=True, kpts=kpts, steps=3, 
                                        orig_shape=vis_image.shape[:2])
                return vis_image



    def estimate_pose(frame, model):
        image, vis_image = PoseEstimation.prepare_image_for_prediction(frame)
        preds = PoseEstimation.predict(image, model)
        out_image = PoseEstimation.visualize_predictions(preds, vis_image)
        return out_image

