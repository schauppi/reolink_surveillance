import socket
import cv2
import pickle
import struct

class JetsonNanoServer():

        def send_message(frame, client_socket):
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a)) + a
                client_socket.sendall(message)


        
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
                                        #Check for Objets every 100 Frames
                                        if i % 50 == 0:
                                                frame, person_counter = object_det_instance.detect_objects(frame)
                                                JetsonNanoServer.send_message(frame, client_socket)
                                                if person_counter > 0:
                                                        while person_counter > 0:
                                                                _, frame = cap.read()
                                                                frame, person_counter = object_det_instance.detect_objects(frame)
                                                                JetsonNanoServer.send_message(frame, client_socket)
                                                else:
                                                        _, frame = cap.read()
                                                        JetsonNanoServer.send_message(frame, client_socket)
                                        else:
                                                frame = frame
                                        print("no person")
                                        JetsonNanoServer.send_message(frame, client_socket)
                                        
                                client_socket.close()
                                cap.release()
                                cv2.destroyAllWindows()
                        except ConnectionResetError:
                                client_socket.close()
                                cap.release()