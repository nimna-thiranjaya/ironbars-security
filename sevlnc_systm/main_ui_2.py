import sys

import numpy
from PyQt5 import QtWidgets,Qt
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5 import QtGui,QtWidgets,QtCore
import numpy as np
import cv2
import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import sys
from PyQt5 import QtWidgets,Qt
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap,QImage
from PyQt5 import QtGui
import cv2
from PyQt5 import QtGui,QtWidgets,QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import cv2
import sys
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication,QTableWidgetItem
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import imutils
from PyQt5 import QtWidgets, QtGui
import os
from datetime import datetime,date
import datetime
import time
import sounddevice as sd
import soundfile as sf
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime
from PyQt5.QtCore import QTimer

from abnomal_detect_restArea import restArea
from abnomal_detect_walking import skaliton_tracking
# from convers_face_abnormal import conversFace
# from convers_audio_abnormal import convers_audAbnomal
from fight_detection_video_base import fightVdetct
from fight_detection_audio_base import predict_audio

# from wepon_detection_main import weponDetect
# from wepon_knif_detection_main import

from wepon_detection_yolo import predict_image as weponDetect
from wepon_knif_detection_yolo import predict_image as knifDetect

from face_recog_main import detect_person as preis_detection

audio_triger_buffer = ''



class Thread(QThread):

    def __init__(self,name):
        super().__init__()
        self.video_name = name

        self.cap = cv2.VideoCapture(self.video_name)

        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))

        print('frame demention - ', height, width)

        # for x in range(10):
        #     ret, frame = self.cap.read()
        #     cv2.waitKey(1)


    def val_handeler(self, b_point):
        self.val = b_point



    def table_clear_handler(self): # clear table

        self.action_triger = False
        self.recode_action_lock = False
        self.triger_chart = []




    def append_name(self, name):
        if name not in self.action_triger_face:
            self.action_triger_face.append(name)

            if self.val == 0:
                detection = 'Anomaly detected'
            if self.val == 1:
                detection = 'Fight detected'
            if self.val == 2:
                detection = 'weapons detected'
            if self.val == 3:
                detection = 'Anomaly detected'

            now = datetime.now()
            date_string = now.strftime('%Y-%m-%d %H:%M:%S')

            data_apend = [detection,name,date_string]

            self.triger_chart.append(data_apend)
            #MainWindow.detection_note()


    changePixmap = pyqtSignal(QImage)

    def run(self):
        #cap = cv2.VideoCapture(self.video_name)
        #cap = cv2.VideoCapture(0)
        #cap = cv2.VideoCapture('fight.mp4', cv2.CAP_GSTREAMER)

        self.last_val = -1
        self.action_triger = False
        self.action_triger_face = []
        self.recode_action_lock = False

        self.triger_chart = []

        self.last_face = ''




        while True:
            ret, frame = self.cap.read()

            frame = cv2.resize(frame, (848,480), interpolation=cv2.INTER_AREA)

            if ret:

                if self.last_val != self.val:

                    self.last_val = self.val
                    self.action_triger = False
                    self.recode_action_lock = False
                    print('clear action triger lock')


                if self.action_triger == True:

                    if self.recode_action_lock == False:

                        if self.val == 0:
                            detection = 'Anomaly detected'
                        if self.val == 1:
                            detection = 'Fight detected'
                        if self.val == 2:
                            detection = 'weapons detected'
                        if self.val == 3:
                            detection = 'Anomaly detected'

                        now = datetime.now()
                        date_string = now.strftime('%Y-%m-%d %H:%M:%S')

                        data_apend = [detection, "------", date_string]
                        self.triger_chart.append(data_apend)
                        print(data_apend)
                        #MainWindow.detection_note()

                        self.recode_action_lock = True

                        #MainWindow.detection_note()


                    frame, detels = preis_detection(frame, anotate=False)

                    if detels != 'no one detect' and detels != 'Unknown':

                        if self.last_face != detels:

                            self.append_name(detels)
                            self.last_face = detels





                if self.val == 0:
                    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    frame, resArea_flag = restArea(frame, anotation=False, detels=False, rect_overlayer=False)
                    frame, abWalking_flag = skaliton_tracking(frame, anotation=False, detels=False)

                    if resArea_flag:

                        detect = "resArea_flag"
                        self.action_triger = True



                    # cam_location = 'room1'
                    # frame = cv2.putText(frame, cam_location, (50,50), cv2.FONT_HERSHEY_SIMPLEX,1, (255, 0, 0), 2, cv2.LINE_AA)






                if self.val == 1:
                    #frame = frame
                    frame, fight_state = fightVdetct(frame, detels=False)

                    #print('fight_state - ',fight_state)

                    if fight_state == 'fight':
                        # print('fight_state - ', fight_state)
                        # detect = 'fight'
                        self.action_triger = True



                    # cam_location = 'front'
                    # frame = cv2.putText(frame, cam_location, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2,cv2.LINE_AA)






                if self.val == 2:

                    frame, wepon_deetels = weponDetect(frame, anotation=False, rect_overlayer=True, detels=False)

                    frame, knif_deetels = knifDetect(frame, anotation=False, rect_overlayer=True, detels=False)


                    print('knif_deetels - ' , knif_deetels.shape[0])

                    if knif_deetels.shape[0] > 0:
                        self.action_triger = True

                    if wepon_deetels.shape[0] > 0:
                        self.action_triger = True




                    #print('wepon_deetels - ',wepon_deetels)
                    # cam_location = 'side room'
                    # frame = cv2.putText(frame, cam_location, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2,cv2.LINE_AA)






                cv2.waitKey(30)
                ####################################################################################################################
                
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)





class audio_capture(QThread):

    def __init__(self):
        super().__init__()




    audio_frame = pyqtSignal(list)

    def run(self):

        while True:

            # Parameters
            duration = 10  # duration of recording in seconds
            sample_rate = 44100  # typical sample rate for audio

            print("Recording...")
            audio_clip = self.record_audio(duration, sample_rate)
            #print("Recorded 10 seconds of audio.")
            #print(audio_clip)

            sf.write('fight_buffer_aud.wav', audio_clip, sample_rate)

            time.sleep(1)  # use machin larning task
            ss = predict_audio('fight_buffer_aud.wav')


            os.remove('fight_buffer_aud.wav')
            print('remove past buffer')

            print('audio_base_fight - ', ss)


            resalt = ['Normal']

            if ss == 'fight':

                #resalt = 'fight audio detect'

                now = datetime.now()
                date_string = now.strftime('%Y-%m-%d %H:%M:%S')

                resalt = ['Fight Audio detected', "---A---", date_string]

                #global audio_triger_buffer
                #audio_triger_buffer = ['detection', "---t---", 'date_string']

                # data_apend = ['detection', "---t---", 'date_string']
                # MainWindow.cam1.triger_chart.append(data_apend)
            self.audio_frame.emit(resalt)




    def record_audio(self,duration, sample_rate):
        """Record audio for a given duration and sample rate, then return as a numpy array."""
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype=np.float32)
        sd.wait()  # Wait until recording is finished
        return audio_data





class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("main_system.ui",self)

        self.initUI()

        self.abnomal.toggled.connect(self.on_radio_button_checked)
        self.fight.toggled.connect(self.on_radio_button_checked)
        self.wepon.toggled.connect(self.on_radio_button_checked)
        #self.clear_detction.connect(self.clear_table) # clear table

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_label)
        self.timer.start(1000)

        self.detec_list.setColumnWidth(0, 100)
        self.detec_list.setColumnWidth(1, 100)
        self.detec_list.setColumnWidth(2, 100)
        self.detec_list.setColumnWidth(3, 100)

        #self.detection_note()

    def on_radio_button_checked(self):
        if self.abnomal.isChecked():
            self.cam1.val_handeler(0)
            print(1)
        elif self.fight.isChecked():
            self.cam1.val_handeler(1)
            print(2)
        elif self.wepon.isChecked():
            self.cam1.val_handeler(2)
            print(3)


    def clear_table(self):
        self.cam1.table_clear_handler(self)  # clear table



    def initUI(self):

        self.aud1 = audio_capture()
        self.aud1.audio_frame.connect(self.set_audio)
        self.aud1.start()

        self.cam1 = Thread(0)

        #time.sleep(5)

        self.cam1.val_handeler(0)
        self.cam1.changePixmap.connect(self.setImage)
        self.cam1.start()
        self.show()




    def setImage(self, image):

        self.camara.setPixmap(QPixmap.fromImage(image)) # salf.[label name]


    def set_audio(self,audio_clip_figth_detect):

        # now = datetime.now()
        # date_string = now.strftime('%Y-%m-%d %H:%M:%S')
        #data_apend = [audio_clip_figth_detect, "-------", date_string]

        if len(audio_clip_figth_detect)>1:
            self.cam1.triger_chart.append(audio_clip_figth_detect)

        print(audio_clip_figth_detect)


    def update_label(self):

        data = self.cam1.triger_chart


        if len(data) > 0:
            #print('im in main classss - ', data)

            #Set the number of rows and columns in the table
            self.detec_list.setRowCount(len(data))
            self.detec_list.setColumnCount(len(data[0])+1)

            self.detec_list.setColumnWidth(0, 120)
            self.detec_list.setColumnWidth(1, 120)
            self.detec_list.setColumnWidth(2, 120)
            self.detec_list.setColumnWidth(3, 120)


            location = 'front door'

            numr = 0
            # Fill the table with data
            for row in range(len(data)):
                for col in range(len(data[row])):
                    self.detec_list.setItem(row, col, QTableWidgetItem(data[row][col]))
                self.detec_list.setItem(numr, 3, QTableWidgetItem(location))

                numr = numr + 1





app=QApplication(sys.argv)
mainwindow=MainWindow()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1369)
widget.setFixedHeight(761)
widget.show()
app.exec_()














# self.pushButton_3.clicked.connect(self.button_clickeda)
# self.next_pg.clicked.connect(self.button_clickeds)

# self.label.setText('current_time')
#
# self.timer = QtCore.QTimer()
# self.timer.timeout.connect(self.update_label)
# self.timer.start(1000)  # every 10,000 milliseconds

# def update_label(self):
#
#     print('sss')
#
#     current_time = str(datetime.datetime.now().time())
#     self.label.setText(current_time)

# def dropImage(self, image):
#
#     pass
#
#
# def button_clickeds(self):
#     print("Buttffon clicked!")
#     self.cam1.changePixmap.connect(self.setImage)
#     self.cam2.changePixmap.connect(self.dropImage)
#
# def button_clickeda(self):
#     print("Buttoggn clicked!")
#     self.cam1.changePixmap.connect(self.dropImage)
#     self.cam2.changePixmap.connect(self.setImage)