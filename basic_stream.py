from handler.credention_handler import CredentionHandler
import cv2



"""cap_cam_1 = cv2.VideoCapture(ip_cam_1)

while(True):
    _, frame_cam_1 = cap_cam_1.read()
    cv2.imshow("CAM1", frame_cam_1 )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break"""

if __name__ == "__main__":
    CredentionHandler()
    username_cam_1, password_cam_1, ip_cam_1  = CredentionHandler.load_credentials(0)
    print(username_cam_1, password_cam_1, ip_cam_1)
