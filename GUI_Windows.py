from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title("Luganda Keyword Spotter")
root.geometry('350x300')
root.columnconfigure(0, weight=1)

#root.configure(background='black')

def audio():
    
    import pyaudio
    import wave

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 2
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")
    
    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def predictor():
    import os
    from keyword_spotting_service import Keyword_Spotting_Service
    
   #global predicted_keyword
    
    def predict():
        audio_file = "output.wav"
        
        #invoke kwSS
        kss =Keyword_Spotting_Service() 
        
        #make a prediction
        global predicted_keyword
        predicted_keyword = kss.predict(audio_file)
        #remove the audio file  
        os.remove(audio_file)
        
        #send back predicted keyword
        print(predicted_keyword)
    predict()
    d = Label(root, text = "Ekigambo Ekivunukidwa: "+ predicted_keyword, padx=50, pady=5,borderwidth=5 ).grid(row=2, column=0)
    
def command():
   def sawa_meka():
       import time
       t = time.localtime()
       current_time = time.strftime("%H:%M:%S", t)
       messagebox.showinfo("Sawa meka", current_time)
    
   def gulawo():
       import os
       path = "C:/Users"
       path = os.path.realpath(path)
       os.startfile(path)
    
   def galawo():
       return
    
   def soma():
       return
    
   def kuba():
       return
    
   def tekako():
       return
   
   def gyako():
       return
    
   def ddamu():
       return
   
   def kendeza():
       from ctypes import cast, POINTER
       from comtypes import CLSCTX_ALL
       from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
       import math

       # Get default audio device using PyCAW
       devices = AudioUtilities.GetSpeakers()
       interface = devices.Activate(
           IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
       volume = cast(interface, POINTER(IAudioEndpointVolume))

       # Get current volume 
       currentVolumeDb = volume.GetMasterVolumeLevel()
       volume.SetMasterVolumeLevel(currentVolumeDb - 6.0, None)
       # NOTE: -6.0 dB = half volume !
   
   def yongeza():
       from ctypes import cast, POINTER
       from comtypes import CLSCTX_ALL
       from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
       import math

       # Get default audio device using PyCAW
       devices = AudioUtilities.GetSpeakers()
       interface = devices.Activate(
           IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
       volume = cast(interface, POINTER(IAudioEndpointVolume))

       # Get current volume 
       currentVolumeDb = volume.GetMasterVolumeLevel()
       volume.SetMasterVolumeLevel(currentVolumeDb + 6.0, None)
   
   def sindika():
       return
   
   def tandika():
       return
   
   def yaka():
       return
   
   def zikira():
       root.quit()
   
   def vaako():
       return
    
   def numbers():
       numbers = print("Please select a command rather than a number")
       messagebox.showinfo("number detected", "Please select a command rather than a number")
    
   if predicted_keyword == "sawa_meka" :
       sawa_meka()   
   elif predicted_keyword == "gulawo" :
       gulawo()
   elif predicted_keyword == "ddamu":
       ddamu()
   elif predicted_keyword == "kuba":
       kuba()
   elif predicted_keyword == "yaka":
       yaka()
   elif predicted_keyword == "vaako":
       vaako()
   elif predicted_keyword == "tandika":
       tandika()
   elif predicted_keyword == "yongeza":
       yongeza()
   elif predicted_keyword == "zikira":
       zikira()
   elif predicted_keyword == "galawo":
       galawo()
   elif predicted_keyword == "tekako":
       tekako()
   elif predicted_keyword == "gyako":
       gyako()
   elif predicted_keyword == "soma":
       soma()
   elif predicted_keyword == "sindika":
       sindika()
   elif predicted_keyword == "kendeza":
       kendeza() 
   elif predicted_keyword in  ("zeero","emu","biri", "satu","nnya","tano","mukaga","musanvu","munana","mwenda","kumi"):
       numbers()
   else:
       print("command not available")
 

    
#Adding image for record button
image =Image.open("audio.jpg")
photo = ImageTk.PhotoImage(image)

l = Label(root, image=photo)
l.bind("<Button-1>")


q = Button(root, image=photo, padx=90, pady=9, borderwidth=5, command = audio )
b = Button(root, text="Vvunula", padx=40, pady=5, borderwidth=5, command = predictor )
c = Button(root, text="Kola", padx=40, pady=5, borderwidth=5, command = command)

q.grid(row=0, column=0)
b.grid(row=1, column=0)
c.grid(row=3, column=0)

root.mainloop()
 
