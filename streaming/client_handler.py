import socket
import cv2
import pickle
import struct
import base64
import numpy as np

class Client():

    def start(host_ip):

        BUFF_SIZE = 65536
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
        port = 10050
        host_ip_str = str(host_ip)
        message = b'Hello'
        client_socket.sendto(message, (host_ip, port))

        while True:
            packet,_ = client_socket.recvfrom(BUFF_SIZE)
            data = base64.b64decode(packet,' /')
            npdata = np.fromstring(data,dtype=np.uint8)
            frame = cv2.imdecode(npdata,1)
            cv2.imshow("RECEIVING VIDEO",frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
                break

        cv2.destroyAllWindows()
        client_socket.close()
    
         





"""        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

        client_socket.close()"""
        