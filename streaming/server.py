import socket
import cv2
import pickle
import struct


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
                        img, frame = cap.read()
                        a = pickle.dumps(frame)
                        message = struct.pack("Q", len(a)) + a
                        client_socket.sendall(message)
                        #cv2.imshow("Sending...", frame)
                        #key = cv2.waitKey(10)
                        #if key == 13:
                client_socket.close()
                cap.release()
                cv2.destroyAllWindows()
        except ConnectionResetError:
                client_socket.close()
                cap.release()