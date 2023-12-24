import torch
import pandas
import cv2
import numpy as np
import imutils
from imutils.video import FPS
import random
import time
import matplotlib


# Model
model = torch.hub.load('ultralytics/yolov5','custom', path="abnomal_detect_restArea_modle.pt")


prev_frame_time = 0
new_frame_time = 0

def predict_image(rim,anotation = True,rect_overlayer = True,detels = True):

    global prev_frame_time,new_frame_time



    #rim = imutils.resize(rim,width=500)
    results = model(rim)

    if detels:
        print(results.pandas().xyxy)
        pass

    obiect_list = results.xyxy
    obiect_list = obiect_list[0].numpy()

    for obj in range(obiect_list.shape[0]):


        #print(obiect_list[obj])

        try:
            if rect_overlayer:

                xmin, ymin, xmax, ymax, confidence, clas = obiect_list[obj]

                if int(clas) == 0 and float(confidence) > 0.4 :
                    xmin,ymin,xmax,ymax,confidence,clas = obiect_list[obj].astype(int)
                    rim = cv2.rectangle(rim, (xmin,ymin), (xmax,ymax), (0,0,255), 3)
        except:
            #print('no object')
            pass

    new_frame_time = time.time()
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time


    fps = int(fps)
    fps = str(fps)
    cv2.putText(rim, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)

    if anotation:
        cv2.imshow('live',rim)
    #cv2.waitKey(1)

    return (rim,obiect_list)


#
# # #cap = cv2.VideoCapture('cat.mp4')
# #
# while True:
#     #r, rim = cap.read()
#     rim = cv2.imread('images/Screenshot (26).png')
#     img , det = predict_image(rim,anotation=False)
#     img = imutils.resize(img,width=500)
#     cv2.imshow('live',img)
#
#     print(det)


