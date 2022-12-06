from handler.credention_handler import CredentionHandler
from handler.stream_handler import StreamingHandler
from handler.streaming_url_handler import CreateStreamingUrl
from pose_estimation.pose_estimation_handler import PoseEstimation
from object_detection.object_detection_handler import ObjectDetection
from streaming.client_handler import Client


def start_clients(jetson_ips):

    for ip in jetson_ips:
        Client.start(ip)


def main(jetson_ips):
    username_cam_1, password_cam_1, ip_cam_1  = CredentionHandler.load_credentials(cam = 0)
    streaming_url_cam_1 = CreateStreamingUrl.create_streaming_url(username_cam_1,
                                                                    password_cam_1,
                                                                    ip_cam_1)

    start_clients(jetson_ips)


if __name__ == "__main__":

    jetson_ips = ["192.168.0.146"]

    main(jetson_ips)



