from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision




def draw_landmarks_on_image(rgb_image, detection_result):
  pose_landmarks_list = detection_result.pose_landmarks
  annotated_image = np.copy(rgb_image)


  for idx in range(len(pose_landmarks_list)):
    pose_landmarks = pose_landmarks_list[idx]


    pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    pose_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
    ])
    solutions.drawing_utils.draw_landmarks(
      annotated_image,
      pose_landmarks_proto,
      solutions.pose.POSE_CONNECTIONS,
      solutions.drawing_styles.get_default_pose_landmarks_style())
  return annotated_image


base_options = python.BaseOptions(model_asset_path='abnomal_detect_pose_landmarker.task')
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    output_segmentation_masks=True)
detector = vision.PoseLandmarker.create_from_options(options)



def skaliton_tracking(frame, anotation = True ,detels = True):

    global detector

    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    detection_result = detector.detect(image)
    annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)

    if anotation:
        cv2.imshow('pros',annotated_image)
    cv2.waitKey(1)

    abnomal_detection_flg = False

    try:
        point = detection_result.pose_landmarks[0][0]  #nose
        x_n = point.x
        y_n = point.y
        z_n = point.z

        #print(f"X: {x_n}, Y: {y_n}, Z: {z_n}")

        point = detection_result.pose_landmarks[0][28] #l leg
        x_l = point.x
        y_l = point.y
        z_l = point.z

        #print(f"X: {x_l}, Y: {y_l}, Z: {z_l}")

        point = detection_result.pose_landmarks[0][27] #r leg
        x_r = point.x
        y_r = point.y
        z_r = point.z

        #print(f"X: {x_r}, Y: {y_r}, Z: {z_r}")


        cal1 = y_l - y_n
        cal2 = y_r - y_n

        if detels:
            print(cal1 , cal2)

        tol = 0.17

        if cal1 < tol or cal2 < tol:
            abnomal_detection_flg = True
            if detels:
                print('abnomal detect')


    except:
        if detels:
            print('no person')



    return annotated_image , abnomal_detection_flg






# cap = cv2.VideoCapture('my dataset/abn_cha.mp4')
#
# while True:
#     r,frame = cap.read()
#
#     #frame = cv2.imread('2 people walking.jpg')
#
#     ano_frae,flg = skaliton_tracking(frame,anotation=False)
#
#     cv2.imshow('fin',ano_frae)
#     cv2.waitKey(1)

