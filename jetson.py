
from streaming.server_handler import JetsonNanoServer
from object_detection.object_detection_handler import ObjectDetection

object_det_instance = ObjectDetection()

JetsonNanoServer.start(object_det_instance)

