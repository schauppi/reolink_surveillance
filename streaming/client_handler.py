import socket
import cv2
import pickle
import struct

class Client():

    def start(host_ip):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_ip = host_ip
        host_ip_str = str(host_ip)
        port = 10050
        client_socket.connect((host_ip, port))

        data = b""

        payload_size = struct.calcsize("Q")

        while True:
            try:
                while len(data) < payload_size:
                    packet = client_socket.recv(4*1024)
                    if not packet: break
                    data += packet
                packet_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packet_msg_size)[0]
                while len(data) < msg_size:
                    data += client_socket.recv(4*1024)

                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                cv2.imshow(host_ip_str, frame)
                key = cv2.waitKey(10)
                if key == 13:
                    break
            except struct.error:
                print("Error opening Camera")
                break

        client_socket.close()