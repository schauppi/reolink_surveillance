import socket
import cv2
import base64
import threading
from queue import Queue


class JetsonClient():

    def __init__(self, url_cam_1, url_cam_2, server_ip, object_det_instance):
        self.url_cam_1 = url_cam_1
        self.url_cam_2 = url_cam_2
        self.server_ip = server_ip
        self.object_det_instance = object_det_instance

    def start(self):

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        cap_cam_1 = cv2.VideoCapture(self.url_cam_1)
        cap_cam_2 = cv2.VideoCapture(self.url_cam_2)

        frame_counter = 0
        tick_count = 0

        tick_count = cv2.getTickCount()

        while True:

            # read a frame 
            _, frame_cam_1 = cap_cam_1.read()
            _, frame_cam_2 = cap_cam_2.read()

            if self.object_det_instance is not "None":
                frame, person_counter = self.object_det_instance.detect_objects(frame)
            elif self.object_det_instance is "None":
                frame = frame_cam_1

            frame_counter += 1
            elapsed_time = (cv2.getTickCount() - tick_count) / cv2.getTickFrequency()

            fps = frame_counter / elapsed_time
            cv2.putText(frame, "FPS Jetson: " + str(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # encode the frame 
            _,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
            message = base64.b64encode(buffer)

            # send the frame over UDP
            client_socket.sendto(message, (self.server_ip, 5000))

            # check if the user pressed the "q" key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # release the webcam and close the socket
        cap_cam_1.release()
        cap_cam_2.release()
        client_socket.close()


"""
Capture Thread for open cv - put the frames in a queue
Detection Thread - get the frames from the queue and do the detection
UDP Thread - send the frames over UDP
"""

"""class JetsonClient():

    def __init__(self, url, server_ip, object_det_instance):
        self.frame_queue = Queue()
        self.detected_frame_queue = Queue()
        self.lock = threading.Lock()
        self.stop_flag = threading.Event()
        self.url = url
        self.server_ip = server_ip
        self.object_det_instance = object_det_instance

    def capture_thread(self):
        while not self.stop_flag.is_set():
            while True:
                cap = cv2.VideoCapture(self.url)

                _, frame = cap.read()

                with self.lock:
                    self.frame_queue.put(frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()

    def detection_thread(self):
        while not self.stop_flag.is_set():
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
        while not self.stop_flag.is_set():
    
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

        try:

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            capture_thread = threading.Thread(target=JetsonClient.capture_thread, args=(self,))
            detection_thread = threading.Thread(target=JetsonClient.detection_thread, args=(self,))
            udp_thread = threading.Thread(target=JetsonClient.udp_thread, args=(self, client_socket))

            capture_thread.start()
            detection_thread.start()
            udp_thread.start()

        except KeyboardInterrupt:
            self.stop_flag.set()
"""


        

        

    