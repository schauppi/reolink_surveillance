import socket
import cv2
import base64

class JetsonClient():

    def start(object_det_instance, url, img_size):

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        cap = cv2.VideoCapture(url)

        while True:

            # read a frame 
            ret, frame = cap.read()

            # encode the frame 
            _,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
            message = base64.b64encode(buffer)

            # send the frame over UDP
            client_socket.sendto(message, ('127.0.0.1', 5000))

            # check if the user pressed the "q" key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # release the webcam and close the socket
        cap.release()
        client_socket.close()