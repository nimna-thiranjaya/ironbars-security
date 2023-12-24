
import cv2
import imutils

from convers_face_abnormal import conversFace
from convers_audio_abnormal import convers_audAbnomal


cap = cv2.VideoCapture('smil.mp4')

# audio_file = 'normal-voice.wav'
# convers_abnomal_flag ,abnomal_word = convers_audAbnomal(audio_file,detels=False)
#
# print(convers_abnomal_flag ,abnomal_word )


while True:
    r, cam_live = cap.read()

    cam_live , dominant_emotion = conversFace(cam_live,detels = False)
    print(dominant_emotion)


    cam_live = imutils.resize(cam_live, width=500)
    cv2.imshow('live', cam_live)
    cv2.waitKey(25)