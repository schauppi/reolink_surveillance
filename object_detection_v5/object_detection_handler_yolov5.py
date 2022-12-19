import sys
sys.path.insert(0, './object_detection_v5')
#sys.path.append('../')

import torch
import numpy as np
import random
import cv2

from handler.image_preparation_handler import ImagePreparation
from utils.general import non_max_suppression
from object_detection_v5.models.experimental import attempt_load
from handler.plot_handler import HandlePlot

device = "cuda"

class ObjectDetectionv5():

        def __init__(self) -> None:
                #try:
                #self.model = torch.hub.load('', model='custom', path='/model_weights/yolov5s.pt', source='local')
                self.model = attempt_load('/model_weights/yolov5s.pt', map_location=torch.device(device))
                self.model.to(device)
                self.model.eval()
                #warmup
                image = torch.rand(1, 3, 640, 640).to(device)
                with torch.inference_mode():
                        self.model(image)
                        print("Object Detection Model loaded sucessfully")
                #except:
                 #       print("Failed loading Object Detection Model")

        def predict(self, image):
                with torch.inference_mode():
                        pred = self.model(image)

                prediction = non_max_suppression(pred)[0].to(device)

                if len(prediction) > 0:
                        return prediction
                else:
                        return None

        
        def detect_objects(self, frame):
                image, original_height, original_width = ImagePreparation.prepare_image(frame, device=device, model="yolov5")
                prediction = self.predict(image)
                if prediction is not None:
                        prediction = ImagePreparation.resize_object_detection_prediction_output(prediction, original_height, original_width)
                        image_with_boxes, person_counter = HandlePlot.plot_bounding_boxes(prediction, frame)
                        return image_with_boxes, person_counter
                else:
                        return frame, 0


"""
model = torch.hub.load('', 'custom', path='model_weights/yolov5s.pt', source='local')
model.to("mps")
print("loaded")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    image_test, height, width = ImagePreparation.prepare_image(frame, device=device, model="yolov5")
    print(image_test.shape)
    tensor_image = torch.rand(1, 3, 640, 640).to(device)
    print(tensor_image.shape)

    results = model(image_test)

    prediction = non_max_suppression(results)[0].to(device)

    prediction = ImagePreparation.resize_object_detection_prediction_output(prediction, height, width)
    image_with_boxes, person_counter = HandlePlot.plot_bounding_boxes(prediction, frame)


    cv2.imshow('Recieving Stream...', image_with_boxes)

    # check if the user pressed the "q" key
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # close the window
    cv2.destroyAllWindows()
"""

