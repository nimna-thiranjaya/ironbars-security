
#from fight_detection_audio_base import predict_audio
import cv2
import imutils

from fight_detection_video_base import fightVdetct


# while True:
#
#     #test_audi = 'fight_3.wav'
#     test_audi = input('enter audio file - ')
#
#     ss = predict_audio(test_audi)
#
#     print('sssss',ss)







cap = cv2.VideoCapture('nomal.mp4')




while True:
    r, cam_live = cap.read()

    cam_live , fight_state = fightVdetct(cam_live,detels=False)
    #print(fight_state)


    cam_live = imutils.resize(cam_live, width=500)
    cv2.imshow('live', cam_live)
    cv2.waitKey(25)