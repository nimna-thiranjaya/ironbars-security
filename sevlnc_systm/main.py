import cv2
import imutils

from abnomal_detect_restArea import restArea
from abnomal_detect_walking import skaliton_tracking
# from convers_face_abnormal import conversFace
# from convers_audio_abnormal import convers_audAbnomal
from fight_detection_video_base import fightVdetct
from fight_detection_audio_base import predict_audio
from wepon_detection_main import weponDetect


cap = cv2.VideoCapture('walking.mp4')


#convers_abnomal_DSP
#
# audio_file = 'normal-voice.wav'
# convers_abnomal_flag ,abnomal_word = convers_audAbnomal(audio_file,detels=False)
# print(convers_abnomal_flag ,abnomal_word )

# fight_audio_DSP
# while True:
#
#     #test_audi = 'fight_3.wav'
#     test_audi = input('enter audio file - ')
#
#     ss = predict_audio(test_audi)
#
#     print('sssss',ss)




while True:
    r, cam_live = cap.read()

    cam_live, resArea_flag = restArea(cam_live,anotation=False,detels=False,rect_overlayer=False)
    cam_live, abWalking_flag = skaliton_tracking(cam_live, anotation=False , detels=False)

    #cam_live, dominant_emotion = conversFace(cam_live, detels=False)

    cam_live, fight_state = fightVdetct(cam_live, detels=False)

    cam_live, wepon_deetels = weponDetect(cam_live, anotation=False, rect_overlayer=True, detels=False)

    cam_live = imutils.resize(cam_live, width=500)
    cv2.imshow('live', cam_live)
    cv2.waitKey(1)