import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
import moviepy.editor as mp
from googletrans import Translator
import numpy as np
import cv2
import win32api
import pandas as pd
from tkinter import * 
from tkinter.ttk import *
from tkinter.filedialog import askopenfile 


def get_large_audio_transcription(path):
    r = sr.Recognizer() 
    sound = AudioSegment.from_wav(path)  
    chunks = split_on_silence(sound,min_silence_len = 500,silence_thresh = sound.dBFS-14,keep_silence=500)
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    for i, audio_chunk in enumerate(chunks, start=1):
   
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("No Voice recognized", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    
    return whole_text

root = Tk() 
root.geometry('200x100') 
  
def open_file():
    
    file = askopenfile(mode ='r', filetypes =[('Video Files', '*.mp4')]) 
    print(file.name)
    clip = mp.VideoFileClip(file.name)
    clip.audio.write_audiofile(r"audio.wav") 
    path = "audio.wav"
    path1=file.name
    cap = cv2.VideoCapture(path1) 
    if (cap.isOpened()== False):  
      print("Error opening video  file") 
    win32api.MessageBox(0, 'To Close video press key q', 'Info')
    while(cap.isOpened()): 
      ret, frame = cap.read() 
      if ret == True:
        b = cv2.resize(frame,(640,480),fx=20,fy=30, interpolation = cv2.INTER_CUBIC)
        cv2.imshow('Frame', b)
    
        if cv2.waitKey(25) & 0xFF == ord('q'): 
            break
      else:  
        break
 
    cap.release() 
    cv2.destroyAllWindows()
    root.destroy()
    r = sr.Recognizer()
    text=get_large_audio_transcription(path)
    print("\nFull text:", text)
    f= open("program.txt","w+")
    f.write(text)
    f.close()


    translator = Translator()
    bad_chars = [',', '.', '!', "*"] 
    f1 = open('program.txt', 'r')
    if f1.mode == 'r':
        contents = f1.read()
    for i in bad_chars:
        contents = contents.replace(i, '')

    x = contents.split(" ")

    tran=[]
    for i in x:
        result = translator.translate(i, dest='en')
        tran.append(result.text)

    out = map(lambda l:l.lower(), tran) 
    output = list(out)

    data =pd.read_excel("Ingredients.xlsx",sep="\t",header=None)
    y=data.iloc[:,0].tolist()

    out1 = map(lambda z:z.lower(), y) 
    output1 = list(out1)

    print(set(output).intersection(set(output1)))
  
btn = Button(root, text ='Browse', command = lambda:open_file()) 
btn.pack(side = TOP, pady = 10) 
mainloop() 


