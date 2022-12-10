import socket
import cv2
import base64
import threading
from queue import Queue


"""class JetsonClient():

    def start(object_det_instance, url, server_ip):

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        cap = cv2.VideoCapture(url)

        while True:

            # read a frame 
            _, frame = cap.read()

            frame, person_counter = object_det_instance.detect_objects(frame)

            # encode the frame 
            _,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
            message = base64.b64encode(buffer)

            # send the frame over UDP
            client_socket.sendto(message, (server_ip, 5000))

            # check if the user pressed the "q" key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # release the webcam and close the socket
        cap.release()
        client_socket.close()"""


"""
Capture Thread for open cv - put the frames in a queue
Detection Thread - get the frames from the queue and do the detection
UDP Thread - send the frames over UDP
"""

class JetsonClient():

    def __init__(self, url, server_ip, object_det_instance):
        self.frame_queue = Queue()
        self.detected_frame_queue = Queue()
        self.lock = threading.Lock()
        self.url = url
        self.server_ip = server_ip
        self.object_det_instance = object_det_instance

    def capture_thread(self):

        while True:
            cap = cv2.VideoCapture(self.url)

            _, frame = cap.read()

            with self.lock:
                self.frame_queue.put(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()

    def detection_thread(self):

        while True:
            with self.lock:
                if not self.frame_queue.empty():
                    frame = self.frame_queue.get()
                else:
                    continue

            frame, person_counter = self.object_det_instance.detect_objects(frame)

            with self.lock:
                self.detected_frame_queue.put(frame)

    def udp_thread(self, client_socket):
        
        while True:
            with self.lock:
                if not self.detected_frame_queue.empty():
                    frame = self.detected_frame_queue.get()
                else:
                    continue

            _,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
            message = base64.b64encode(buffer)
            client_socket.sendto(message, (self.server_ip, 5000))

    
        client_socket.close()
            

    def start(self):

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        capture_thread = threading.Thread(target=JetsonClient.capture_thread, args=(self,))
        detection_thread = threading.Thread(target=JetsonClient.detection_thread, args=(self,))
        udp_thread = threading.Thread(target=JetsonClient.udp_thread, args=(self, client_socket))

        capture_thread.start()
        detection_thread.start()
        udp_thread.start()

        

        

    