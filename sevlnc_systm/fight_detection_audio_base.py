import librosa
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import os

# Step 1: Preprocess the audio and extract features

# Define the function to extract audio features

svm = 0

def extract_features(file_path):

    print(file_path)
    # Load audio file
    #audio, sr = librosa.load(file_path)
    y, sr = librosa.load(file_path, duration=10, offset=0.5)

    # mfcc = librosa.feature.mfcc(y = audio, sr=sr)
    # mfcc_mean = np.mean(mfcc, axis=1)

    #y, sr = librosa.load(filename, duration=3, offset=0.5)
    mfcc_mean = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)

    return mfcc_mean





def train_svm():

    folder_parth = 'fight_detection_audio_dataset'

    fight_files = os.listdir(folder_parth+'/fight')
    normal_files = os.listdir(folder_parth+'/normal')

    # normal_files = ['normal1.wav', 'normal2.wav', 'normal3.wav']

    # Create an empty list to store the features and labels
    features = []
    labels = []

    # Extract features and assign labels for the "fight" class
    for file in fight_files:
        features.append(extract_features(folder_parth+'/fight/'+file))
        labels.append('fight')

    # Extract features and assign labels for the "happy" class
    # for file in happy_files:
    #     features.append(extract_features(file))
    #     labels.append('happy')

    #Extract features and assign labels for the "normal" class
    for file in normal_files:
        features.append(extract_features(folder_parth+'/normal/'+file))
        labels.append('normal')

    # Step 3: Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

    # Step 4: Train a Support Vector Machine (SVM) classifier
    global svm
    svm = SVC()
    svm.fit(X_train, y_train)

    # Step 5: Evaluate the model
    y_pred = svm.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)


def predict_audio(test_audi):

    # Step 6: Real-time classification (assuming 'audio' contains real-time audio data)
    audio_features = extract_features(test_audi)
    prediction = svm.predict([audio_features])[0]
    print("Predicted class:", prediction)

    return prediction



train_svm()



