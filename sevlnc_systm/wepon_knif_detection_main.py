
import cv2
import imutils

from wepon_knif_detection_yolo import predict_image as weponDetect



cap = cv2.VideoCapture('gun1.mp4')


while True:
    r, cam_live = cap.read()

    cam_live , wepon_deetels = weponDetect(cam_live,anotation = False,rect_overlayer = True,detels = False)

    print(wepon_deetels)


    cam_live = imutils.resize(cam_live, width=500)
    cv2.imshow('live', cam_live)
    cv2.waitKey(25)