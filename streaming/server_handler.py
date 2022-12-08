import socket
import cv2
import pickle
import struct
import base64

class JetsonNanoServer():


        def start(object_det_instance, url, img_size):

                BUFF_SIZE = 65536
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
                port = 10050
                server_socket.bind(('', port))
                #server_socket.listen(5)

                while True:
                        print("Waiting for connections")
                  
                        _, client_addr = server_socket.recvfrom(BUFF_SIZE)
                        print("Got connection from ", client_addr)
                        server_socket.sendto("hello", client_addr)

                      


"""        def send_message(frame, client_socket):
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a)) + a
                client_socket.sendall(message)
                
        def get_frame_from_camera(cap, img_size):
                _, frame = cap.read()
                frame = cv2.resize(frame, (img_size))
                return frame"""

"""
        def start(object_det_instance, url, img_size):
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                #host_name = socket.gethostname()
                #host_ip = socket.gethostbyname(host_name)

                port = 10050
                server_socket.bind(('', port))
                server_socket.listen(5)


                while True:
                        print("Waiting for connections")
                        try:
                                client_socket, addr = server_socket.accept()
                                print("Connection from", addr)
                                i = 0
                                cap = cv2.VideoCapture(url)
                                while(cap.isOpened()):
                                        frame = JetsonNanoServer.get_frame_from_camera(cap, img_size)

                                        i += 1
                                        #Check for Objets every 50 Frames
                                        if i % 50 == 0:
                                                frame, person_counter = object_det_instance.detect_objects(frame)
                                                JetsonNanoServer.send_message(frame, client_socket)
                                                if person_counter > 0:
                                                        while person_counter > 0:
                                                                frame = JetsonNanoServer.get_frame_from_camera(cap, img_size)
                                                                try:
                                                                        frame, person_counter = object_det_instance.detect_objects(frame)
                                                                        JetsonNanoServer.send_message(frame, client_socket)
                                                                        print("person detected")
                                                                        print("--------")
                                                                except:
                                                                        frame = frame
                                                else:
                                                        frame = JetsonNanoServer.get_frame_from_camera(cap, img_size)
                                                        JetsonNanoServer.send_message(frame, client_socket)
                                                        print("no person")
                                                        print("--------")
                                        else:
                                                frame = frame
                                                print("no person")
                                                print("--------")
                                        JetsonNanoServer.send_message(frame, client_socket)
                                        
                                client_socket.close()
                                cap.release()
                                cv2.destroyAllWindows()
                        except ConnectionResetError:
                                client_socket.close()
                                cap.release()"""