#import sys
#sys.path.insert(0, './object_detection')

import torch
import numpy as np
import random

import cv2

device = "mps"


model = torch.hub.load(' ', 'custom', path='/object_detection/model_weights/yolov5s.pt', source='local')

print("loaded")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    results = model(frame)

    print(results.xyxy[0])

    cv2.imshow('Recieving Stream...', frame)

    # check if the user pressed the "q" key
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # close the window
    cv2.destroyAllWindows()


