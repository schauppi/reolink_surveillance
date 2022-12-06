import cv2
import torch 
from torchvision import transforms
import numpy as np

from object_detection.utils.datasets import letterbox

device = "cuda"

class ImagePreparation():

    def prepare_image(frame, image_size=640):
        image = np.asarray(frame)

        #Resize
        original_height, original_width = image.shape[:2]
        image = cv2.resize(image, (image_size, image_size))

        image_pt = torch.from_numpy(image).permute(2, 0, 1).to(device)
        image_pt = image_pt.float() / 255.0

        return image_pt, original_height, original_width

    def resize_object_detection_prediction_output(prediction, original_height, original_width, image_size=640):

        prediction[:, [0, 2]] *= original_width / image_size
        prediction[:, [1, 3]] *= original_height / image_size

        return prediction

    def resize_pose_estimation_prediction_output(prediction, original_height, original_width, image_size=640):
        prediction[:, 0::3] *= original_width / image_size
        prediction[:, 1::3] *= original_height / image_size

        return prediction


