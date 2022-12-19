import socket
import cv2
import base64
import numpy as np

class Server():

        def start():
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

                # bind the socket to a local address
                sock.bind(('', 5000))

                frame_counter = 0
                tick_count = 0

                tick_count = cv2.getTickCount()

                while True:
                        
                        # receive a frame from the client
                        frame, addr = sock.recvfrom(100000)

                        # decode the frame
                        frame = base64.b64decode(frame,' /')
                        npdata = np.fromstring(frame,dtype=np.uint8)
                        frame = cv2.imdecode(npdata,1)

                        frame_counter += 1
                        elapsed_time = (cv2.getTickCount() - tick_count) / cv2.getTickFrequency()
                        cv2.putText(frame, "FPS Server: " + str(frame_counter / elapsed_time), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                        # display the frame
                        cv2.imshow('Recieving Stream...', frame)

                        # check if the user pressed the "q" key
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                                break

                        # close the window
                        cv2.destroyAllWindows()

      