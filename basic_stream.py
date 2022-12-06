from handler.credention_handler import CredentionHandler
from handler.stream_handler import StreamingHandler
from handler.streaming_url_handler import CreateStreamingUrl
from pose_estimation.pose_estimation_handler import PoseEstimation
from object_detection.object_detection_handler import ObjectDetection

import cv2

if __name__ == "__main__":

    """
    Load an Create Instances of the models
    """
    #Pose_Estimation = PoseEstimation()
    Object_Detection = ObjectDetection()


    username_cam_1, password_cam_1, ip_cam_1  = CredentionHandler.load_credentials(cam = 0)
    streaming_url_cam_1 = CreateStreamingUrl.create_streaming_url(username_cam_1,
                                                                    password_cam_1,
                                                                    ip_cam_1)


    while True:
        """
        Implementation for one Camera
        """
        
"""        frame_cam_1 = StreamingHandler.stream(streaming_url_cam_1, cam="CAM1")
        #frame_with_pose = PoseEstimation.detect_poses(frame_cam_1, Pose_Estimation.model)
        frame_with_objects = ObjectDetection.detect_objects(frame_cam_1, Object_Detection.model)

        cv2.imshow("cam", frame_with_objects)
        if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break"""
