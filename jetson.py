from streaming.client_handler import JetsonClient
from object_detection_v7.object_detection_handler_yolov7 import ObjectDetectionv7
from object_detection_v5.object_detection_handler_yolov5 import ObjectDetectionv5

from handler.credention_handler import CredentionHandler
from handler.streaming_url_handler import CreateStreamingUrl


def get_streaming_urls():
    username_cam_1, password_cam_1, ip_cam_1  = CredentionHandler.load_credentials(cam = 0)
    streaming_url_cam_1 = CreateStreamingUrl.create_streaming_url(username_cam_1,
                                                                    password_cam_1,
                                                                    ip_cam_1)

    return streaming_url_cam_1


def main(server_ip):

    url = get_streaming_urls()

    object_det_instance = ObjectDetectionv5()
    Jetson = JetsonClient(url, server_ip, object_det_instance)
    Jetson.start()

if __name__ == "__main__":

    server_ip = '192.168.50.177'

    main(server_ip)
