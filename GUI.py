from tkinter import *
from PIL import Image, ImageTk
root = Tk()
root.title("Luganda Keyword Spotter")
#root.geometry('300x300')
#root.configure(background='black')

def audio():
    
    import pyaudio
    import wave

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
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
    d = Label(root, text = predicted_keyword, padx=50, pady=5,borderwidth=5 ).grid(row=1, column=1)
    
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
       return
   
   def yongeza():
       return
   
   def sindika():
       return
   
   def tandika():
       return
   
   def yaka():
       return
   
   def zikira():
       return
   
   def numbers():
       numbers = print("Please select a command rather than a number")
       messagebox.showinfo("number detected",numbers)
    
   if predicted_keyword == "dataset\sawa_meka" :
       sawa_meka()
      
   elif predicted_keyword == "dataset\gulawo" :
       gulawo()
   else :
       print(...)
 

    
#Adding image for record button
image =Image.open("audio.jpg")
photo = ImageTk.PhotoImage(image)

l = Label(root, image=photo)
l.bind("<Button-1>")


q = Button(root, image=photo, padx=90, pady=9, borderwidth=5, command = audio )
b = Button(root, text="Detect Keyword", padx=40, pady=5, borderwidth=5, command = predictor )
c = Button(root, text="Run Command", padx=40, pady=5, borderwidth=5, command = command)

q.grid(row=0, column=0)
b.grid(row=1, column=0)
c.grid(row=2, column=0)

root.mainloop()
 