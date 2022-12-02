from handler.credention_handler import CredentionHandler
from handler.stream_handler import StreamingHandler
from handler.streaming_url_handler import CreateStreamingUrl
from pose_estimation.pose_estimation_handler import PoseEstimation

import cv2

if __name__ == "__main__":
    CredentionHandler()
    CreateStreamingUrl()
    StreamingHandler()
    Pose_Estimation = PoseEstimation()


    username_cam_1, password_cam_1, ip_cam_1  = CredentionHandler.load_credentials(cam = 0)
    streaming_url_cam_1 = CreateStreamingUrl.create_streaming_url(username_cam_1,
                                                                    password_cam_1,
                                                                    ip_cam_1)

    #pose_estimation_model = PoseEstimation.load_model()

    while True:
        """
        Implementation for one Camera
        """
        frame_cam_1 = StreamingHandler.stream(streaming_url_cam_1, cam="CAM1")
        print(frame_cam_1.shape)
        frame_with_pose = PoseEstimation.estimate_pose(frame_cam_1, Pose_Estimation.model)


        cv2.imshow("cam", frame_with_pose)
        if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break
