import cv2
import numpy as np
from pose_estimation.utils.plots import plot_skeleton_kpts

class HandlePlot():

    def plot_bounding_boxes(prediction, image):

        for pred in prediction:
            #Plot only class person
            if int(pred[5]) == 0:
                c1, c2 = c1, c2 = (int(pred[0]), int(pred[1])), (int(pred[2]), int(pred[3]))
                cv2.rectangle(image, c1, c2, color=(255, 0, 0))
            else:
                pass

        return image


    def plot_pose(prediction, image):
        image = np.asarray(image)

        for pred in range(prediction.shape[0]):
            plot_skeleton_kpts(image, prediction[pred].T, 3)

        return image
