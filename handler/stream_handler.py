import cv2

class StreamingHandler():

    def stream(streaming_url, cam:str):
        
        cap = cv2.VideoCapture(streaming_url)
        _, frame = cap.read()
        return frame

"""        while(True):
            _, frame = cap.read()
            cv2.imshow(cam, frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break"""