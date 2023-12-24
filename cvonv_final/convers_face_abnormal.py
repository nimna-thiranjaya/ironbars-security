

from deepface import DeepFace


def deepface_backandes():

    backends = [
      'opencv',
      'ssd',
      'dlib',
      'mtcnn',
      'retinaface',
      'mediapipe'
    ]


    objs = DeepFace.analyze(img_path = "img4.jpg", actions = ['age', 'gender', 'race', 'emotion'])

    print(objs)

    def represent(img_path, model_name, detector_backend, enforce_detection, align):
        result = {}
        embedding_objs = DeepFace.represent(
            img_path=img_path,
            model_name=model_name,
            detector_backend=detector_backend,
            enforce_detection=enforce_detection,
            align=align,
        )
        result["results"] = embedding_objs
        return result

    def verify(
            img1_path, img2_path, model_name, detector_backend, distance_metric, enforce_detection, align
    ):
        obj = DeepFace.verify(
            img1_path=img1_path,
            img2_path=img2_path,
            model_name=model_name,
            detector_backend=detector_backend,
            distance_metric=distance_metric,
            align=align,
            enforce_detection=enforce_detection,
        )
        return obj

    def analyze(img_path, actions, detector_backend, enforce_detection, align):
        result = {}
        demographies = DeepFace.analyze(
            img_path=img_path,
            actions=actions,
            detector_backend=detector_backend,
            enforce_detection=enforce_detection,
            align=align,
        )
        result["results"] = demographies
        return result

def conversFace(img,detels = False):

    #objs = DeepFace.analyze(img_path = img, actions = ['age', 'gender', 'race', 'emotion'])

    objs = DeepFace.analyze(img_path=img, actions=['emotion'])

    dominant_emotion = objs[0]['dominant_emotion']

    if detels:
        print(dominant_emotion)

    return img , dominant_emotion

















