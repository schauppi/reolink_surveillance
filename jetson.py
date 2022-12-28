
import argparse
from streaming.client_handler import JetsonClient
from handler.credention_handler import CredentionHandler
from handler.streaming_url_handler import CreateStreamingUrl

parser = argparse.ArgumentParser()
parser.add_argument("--detection", default="None", help="Detection model to use")
args = parser.parse_args()


def get_streaming_urls():
    username_cam_1, password_cam_1, ip_cam_1  = CredentionHandler.load_credentials(cam = 1)
    username_cam_2, password_cam_2, ip_cam_2  = CredentionHandler.load_credentials(cam = 2)
    streaming_url_cam_1 = CreateStreamingUrl.create_streaming_url(username_cam_1,
                                                                    password_cam_1,
                                                                    ip_cam_1)

    streaming_url_cam_2 = CreateStreamingUrl.create_streaming_url(username_cam_2,
                                                                    password_cam_2,
                                                                    ip_cam_2)

    return streaming_url_cam_1, streaming_url_cam_2


def main(server_ip, parser_arguments):

    url_cam1, url_cam2 = get_streaming_urls()

    if parser_arguments == "None":
        object_det_instance = "None"
    elif parser_arguments == "yolov5":
        from object_detection_v5.object_detection_handler_yolov5 import ObjectDetectionv5
        object_det_instance = ObjectDetectionv5()
    elif parser_arguments == "yolov7":
        from object_detection_v7.object_detection_handler_yolov7 import ObjectDetectionv7
        object_det_instance = ObjectDetectionv7()

    Jetson = JetsonClient(url_cam1, url_cam2, server_ip, object_det_instance)
    Jetson.start()

if __name__ == "__main__":

    server_ip = '192.168.50.177'

    parser_arguments = args.detection

    main(server_ip, parser_arguments)
