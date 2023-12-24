import time

from PyQt5 import QtWidgets, Qt
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtGui import QImage, QPixmap
import imutils
from PyQt5 import QtWidgets, QtGui
import pyaudio
import wave
import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTableWidgetItem
from PyQt5.QtCore import Qt, QThread, QTimer, pyqtSignal
from datetime import datetime

from convers_face_abnormal import conversFace
from convers_audio_abnormal import convers_audAbnomal
from face_recog_main import detect_person as preis_detection

detect_person_comm = '------'


class audio_processing(QThread):
    audio_abnomal_state = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def run(self):
        time.sleep(2)

        audio_file = 'output.wav'
        convers_abnomal_flag, abnomal_word = convers_audAbnomal(audio_file, detels=False)
        print(convers_abnomal_flag, abnomal_word)

        if convers_abnomal_flag == False:
            now = datetime.now()
            date_string = now.strftime('%Y-%m-%d %H:%M:%S')

            global detect_person_comm

            data_apend = ['conv abnormal', detect_person_comm, date_string]

            self.audio_abnomal_state.emit(data_apend)


class AudioRecorder(QThread):
    recording_finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.sample_rate = 44100
        self.chunk_size = 1024
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False

    def run(self):
        self.is_recording = True
        self.stream = self.audio.open(format=self.audio_format,
                                      channels=self.channels,
                                      rate=self.sample_rate,
                                      input=True,
                                      frames_per_buffer=self.chunk_size)
        frames = []
        while self.is_recording:
            data = self.stream.read(self.chunk_size)
            frames.append(data)

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.save_audio(frames)

    def stop_recording(self):
        self.is_recording = False
        self.recording_finished.emit()

    def save_audio(self, frames):
        output_file = "output.wav"
        with wave.open(output_file, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.audio_format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(frames))


class VideoRecorderThread(QThread):
    recording_finished = pyqtSignal()
    changePixmap = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.triger_chart = []
        self.recording = False
        self.video_out = cv2.VideoWriter()
        self.identiti = '------'
        self.last_imotion = ''

    def reset(self):

        self.triger_chart = []

    def audio_abnomal_apend(self, data):

        self.triger_chart.append(data)

    def run(self):
        # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        # self.video_out = cv2.VideoWriter('video_out.mp4', fourcc, 30.0, (640, 480))

        cap = cv2.VideoCapture(0)  # 0 represents the default camera (you can change it to a specific camera if needed)
        while self.recording:
            ret, frame = cap.read()
            if ret:

                try:

                    frame, dominant_emotion = conversFace(frame, detels=False)

                    frame, detels = preis_detection(frame, anotate=False)
                    if detels != 'no one detect' and detels != 'Unknown':
                        self.identiti = detels

                    print(dominant_emotion)

                    now = datetime.now()
                    date_string = now.strftime('%Y-%m-%d %H:%M:%S')

                    print(date_string)

                    global detect_person_comm

                    detect_person_comm = self.identiti

                    if dominant_emotion == 'angry' and dominant_emotion != self.last_imotion:
                        data_apend = ['angry', self.identiti, date_string]
                        self.triger_chart.append(data_apend)
                        self.last_imotion = dominant_emotion

                    if dominant_emotion == 'sad' and dominant_emotion != self.last_imotion:
                        data_apend = ['sad', self.identiti, date_string]
                        self.triger_chart.append(data_apend)
                        self.last_imotion = dominant_emotion


                except:
                    pass

                cv2.waitKey(10)

                # self.video_out.write(frame)

                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

        cap.release()
        # self.video_out.release()
        self.recording_finished.emit()

    def start_recording(self):
        self.recording = True
        self.start()

    def stop_recording(self):
        self.recording = False


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("conv.ui", self)

        self.stop.clicked.connect(self.stop_recording)
        self.start.clicked.connect(self.start_recording)

        self.recorder = AudioRecorder()
        self.recorder.recording_finished.connect(self.enable_start_button)

        self.recording_thread = VideoRecorderThread()
        # self.recording_thread.recording_finished.connect(self.enable_start_button)

        self.recording_thread.changePixmap.connect(self.setImage)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_label)
        self.timer.start(1000)

        self.aux_pro = audio_processing()
        self.aux_pro.audio_abnomal_state.connect(self.audio_status_update)

    def audio_status_update(self, status):

        print('main eke inne ', status)

        self.recording_thread.audio_abnomal_apend(status)

    def setImage(self, image):

        self.camara.setPixmap(QPixmap.fromImage(image))  # salf.[label name]

    def start_recording(self):
        self.start.setEnabled(False)
        self.stop.setEnabled(True)
        self.recorder.start()
        self.recording_thread.start_recording()

    def stop_recording(self):
        self.stop.setEnabled(False)
        # self.start.setEnabled(True)
        self.recorder.stop_recording()
        self.recording_thread.stop_recording()
        self.aux_pro.start()

    def enable_start_button(self):
        time.sleep(1)
        self.recorder = AudioRecorder()
        self.recorder.recording_finished.connect(self.enable_start_button)
        self.start.setEnabled(True)

    def update_label(self):

        data = self.recording_thread.triger_chart

        if len(data) > 0:
            # print('im in main classss - ', data)

            # Set the number of rows and columns in the table
            self.detec_list.setRowCount(len(data))
            self.detec_list.setColumnCount(len(data[0]))

            self.detec_list.setColumnWidth(0, 150)
            self.detec_list.setColumnWidth(1, 150)
            self.detec_list.setColumnWidth(2, 150)

            # Fill the table with data
            for row in range(len(data)):
                for col in range(len(data[row])):
                    self.detec_list.setItem(row, col, QTableWidgetItem(data[row][col]))


app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1369)
widget.setFixedHeight(761)
widget.show()
app.exec_()
