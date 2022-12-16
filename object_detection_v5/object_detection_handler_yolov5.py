import sys
sys.path.insert(0, './object_detection_v5')
sys.path.append('../')

import torch
import numpy as np
import random

import cv2

from torchsummary import summary

from handler.image_preparation_handler import ImagePreparation

device = "mps"

model = torch.hub.load('', 'custom', path='object_detection_v5/model_weights/yolov5s.pt', source='local')
model.to(device)
print("loaded")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    image_test, _, _ = ImagePreparation.prepare_image(frame, device=device, model="yolov5")

    results = model(image_test)

    cv2.imshow('Recieving Stream...', frame)

    # check if the user pressed the "q" key
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # close the window
    cv2.destroyAllWindows()


