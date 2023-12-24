
import cv2
import imutils

from abnomal_detect_restArea import restArea
from abnomal_detect_walking import skaliton_tracking


cap = cv2.VideoCapture('walking.mp4')


while True:
    r, cam_live = cap.read()

    cam_live, resArea_flag = restArea(cam_live,anotation=False,detels=False,rect_overlayer=False)

    cam_live, abWalking_flag = skaliton_tracking(cam_live, anotation=False , detels=False)



    cam_live = imutils.resize(cam_live, width=500)
    cv2.imshow('live', cam_live)
    cv2.waitKey(25)