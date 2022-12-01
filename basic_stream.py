from handler.credention_handler import CredentionHandler
from handler.stream_handler import StreamingHandler
from handler.streaming_url_handler import CreateStreamingUrl

import cv2

if __name__ == "__main__":
    CredentionHandler()
    CreateStreamingUrl()
    StreamingHandler()

    username_cam_1, password_cam_1, ip_cam_1  = CredentionHandler.load_credentials(cam = 0)
    streaming_url_cam_1 = CreateStreamingUrl.create_streaming_url(username_cam_1,
                                                                    password_cam_1,
                                                                    ip_cam_1)

    while True:
        #grab frames from camera
        frame_cam_1 = StreamingHandler.stream(streaming_url_cam_1, cam="CAM1")
