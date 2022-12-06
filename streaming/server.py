import socket
import cv2
import pickle
import struct

from object_detection.object_detection_handler import ObjectDetection

yolov7_model = ObjectDetection()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)

port = 10050
server_socket.bind(('', port))
server_socket.listen(5)

while True:
        print("Waiting for connections")
        try:
                client_socket, addr = server_socket.accept()
                print("Connection from", addr)
                cap = cv2.VideoCapture(0)
                while(cap.isOpened()):
                        _, frame = cap.read()

                        frame = ObjectDetection.detect_objects(frame, yolov7_model.model)
                        
                        a = pickle.dumps(frame)
                        message = struct.pack("Q", len(a)) + a
                        client_socket.sendall(message)
                client_socket.close()
                cap.release()
                cv2.destroyAllWindows()
        except ConnectionResetError:
                client_socket.close()
                cap.release()