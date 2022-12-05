import cv2

class StreamingHandler():

    def stream(streaming_url, cam:str):

        cap = cv2.VideoCapture(streaming_url)
        sucess, frame = cap.read()
        if sucess == False:
            print("IP-Camera not available")
            cap = cv2.VideoCapture("alter_vid/cyclist.mp4")
            _, frame = cap.read()

        return frame
