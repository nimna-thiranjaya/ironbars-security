import speech_recognition as sr
import librosa, librosa.display
from scipy.io.wavfile import write
import time
import numpy as np

import nltk
#nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

r = sr.Recognizer()






def mp3_to_text(parth,detels = True):

    y, srt = librosa.load(parth)
    samplerate = srt
    y = y * 32767
    data = y
    write("pre_prosess_audio.wav", samplerate, data.astype(np.int16))
    time.sleep(1)

    hellow = sr.AudioFile('pre_prosess_audio.wav')
    with hellow as source:
        audio = r.record(source)
    try:
        s = r.recognize_google(audio)
        if detels:
            print("Text: " + s)
        chaild_text = s
    except Exception as e:
        if detels:
            print("Exception: " + str(e))
        chaild_text = "i cant hear you properly"

    chaild = chaild_text


    return chaild

def convers_audAbnomal(audio_file,detels = True):

    riz = mp3_to_text(audio_file , detels = detels)
    if detels:
        print(riz)



    words_in_quote = word_tokenize(riz)

    if detels:
        print(words_in_quote)


    # f = open("recognized.txt", "r")
    # print(f.read().type())
    # words_list = str(f.read())

    p_words_list = open('convers_criminal_words.txt').read().splitlines()



    #words_list = 'gun,weapon,person,English'

    #p_words_list = words_list.split(',')

    if detels:
        print(p_words_list)


    convers_state = "no abnormality detect in conversation "

    for p_word in p_words_list:

        for t_word in words_in_quote:
            #print("p_word ---- ", p_word, '-----', t_word)

            if str(p_word) == str(t_word) :



                if not str(p_word) == 'a':

                    #print('dddddddddd,',str(p_word) , '--------',str(t_word))

                    convers_state = "abnormality detected detect word is ="+str(t_word)

    if detels:
        print('--------------------------------------')
        print(convers_state)

    convers_abnomal_flag = False

    if convers_state == "no abnormality detect in conversation ":
        convers_abnomal_flag = True

    return convers_abnomal_flag ,convers_state   #---> #abnomal_word




# audio_file = 'normal-voice.wav'
#
# convers_abnomal_flag ,abnomal_word = convers_audAbnomal(audio_file,detels=False)