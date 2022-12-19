import socket
import cv2
import base64
import numpy as np

class Server():

        def start():
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

                # bind the socket to a local address
                sock.bind(('', 5000))

                while True:
                        
                        # receive a frame from the client
                        frame, addr = sock.recvfrom(100000)

                        # decode the frame
                        frame = base64.b64decode(frame,' /')
                        npdata = np.fromstring(frame,dtype=np.uint8)
                        frame = cv2.imdecode(npdata,1)

                        # display the frame
                        cv2.imshow('Recieving Stream...', frame)

                        # check if the user pressed the "q" key
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                                break

                        # close the window
                        cv2.destroyAllWindows()

      