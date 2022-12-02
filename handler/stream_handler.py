import cv2

class StreamingHandler():

    def stream(streaming_url, cam:str):
        
        cap = cv2.VideoCapture(streaming_url)
        _, frame = cap.read()
        return frame
