import cv2
import imutils
import numpy as np
from abnomal_detect_yolo_predict import predict_image
import time





def restArea(cam_live,anotation=False,detels=False , rect_overlayer=False):

    # cam_live = cv2.GaussianBlur(cam_live, (5, 5), 0)
    # cam_live = cv2.GaussianBlur(cam_live, (5, 5), 0)

    # lain



    pts = np.array(np.load('abnomal_detect_restArea_LINES.npy'), np.int32)

    mask_rest_area = np.load('abnomal_detect_restArea_MARKS.npy')

    # pts = np.array(
    #     [[286, 479], [328, 304], [343, 212], [345, 162], [335, 142], [208, 139], [158, 216], [64, 333], [3, 398],
    #      [3, 475]], np.int32)



    cam_live = cv2.polylines(cam_live, [pts], True, (255, 0, 0), 3)



    # pts = np.array(
    #     [[331, 476], [363, 269], [364, 183], [360, 162], [435, 149], [472, 222], [494, 308], [509, 446], [502, 476]],
    #     np.int32)
    # cam_live = cv2.polylines(cam_live, [pts], True, (0, 255, 0), 3)
    #
    # pts = np.array(
    #     [[501, 478], [585, 323], [671, 255], [768, 206], [789, 197], [852, 258], [794, 312], [763, 364], [744, 430],
    #      [735, 476]], np.int32)
    # cam_live = cv2.polylines(cam_live, [pts], True, (0, 255, 0), 3)


    cam_live, det = predict_image(cam_live, anotation=anotation,detels=detels , rect_overlayer=rect_overlayer)
    #print(det)

    Anomaly_detect_key = False

    for person in det:
        #[         xmin        ymin        xmax        ymax  confidence  class      name

        #if int(person[5]) != 0 and int(person[5]) != 25:

        class_track = int(person[5])

        if person[4] > 0.3 and (abs(person[0] - person[2]) < 300):

            if True : #filter class

                #print(person)
                x1, y1 = int(person[0]),int(person[1])
                x2, y2 = int(person[2]),int(person[3])

                cam_live = cv2.rectangle(cam_live, (x1, y1), (x2, y2), (0, 0, 255), 3)

                mid_point = int((x1 + x2) / 2), int((y1 + y2) / 2)


                try:
                    wt , hi , ss = cam_live.shape
                    print(wt , hi , ss)

                    circle_mask = np.zeros((wt, hi), dtype=np.uint8)
                    person_mid_point = cv2.circle(circle_mask, (mid_point), 20, 255, -1)

                    mask_rest_area_optz = cv2.resize(mask_rest_area, (hi, wt))


                    print(mask_rest_area_optz.shape, '  -  ' , person_mid_point.shape)



                    intersection = cv2.bitwise_and(mask_rest_area_optz, person_mid_point)

                    # cv2.imshow('area',mask_rest_area_optz)
                    # cv2.imshow('person', person_mid_point)
                    # cv2.imshow('intersect', intersection)
                    #
                    # cv2.waitKey(1)

                except:
                    pass


                # if (int((x1 + x2) / 2) < 340) and (int((y1 + y2) / 2) > 150):
                #     cv2.circle(cam_live, mid_point, 10, (255, 0, 0), -1)
                #     cam_live = cv2.putText(cam_live, 'Anomaly detect', (50,50), cv2.FONT_HERSHEY_SIMPLEX,2, (255,0,0), 2, cv2.LINE_AA)

                if cv2.countNonZero(intersection) > 0:

                    Anomaly_detect_key = True




    return cam_live ,Anomaly_detect_key

    # cam_live = imutils.resize(cam_live, width=500)
    # cv2.imshow('live', cam_live)
    # cv2.waitKey(25)