import socket
import cv2
import pickle
import struct

class JetsonNanoServer():

        def start(object_det_instance):
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
                                i = 0
                                cap = cv2.VideoCapture(0)
                                while(cap.isOpened()):
                                        _, frame = cap.read()
                                        i += 1
                                        print(i)
                                        if i / 1000 == 0:
                                                frame = object_det_instance.detect_objects(frame)
                                        else:
                                                frame = frame
                                        a = pickle.dumps(frame)
                                        message = struct.pack("Q", len(a)) + a
                                        client_socket.sendall(message)
                                client_socket.close()
                                cap.release()
                                cv2.destroyAllWindows()
                        except ConnectionResetError:
                                client_socket.close()
                                cap.release()