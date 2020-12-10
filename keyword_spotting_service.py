import tensorflow.keras as keras
import numpy as np
import librosa 

model_path = "model.h5"
NUM_SAMPLES_TO_CONSIDER = 44100 # with sample rate = 1 second of sound


class _Keyword_Spotting_Service: #class can only have 1 instance in a program, singleton
    
    model = None
    _mappings = [
        "biri",
        "ddamu",
        "emu",
        "galawo",
        "gulawo",
        "gyako",
        "kendeza",
        "kuba",
        "kumi",
        "mukaga",
        "munana",
        "musanvu",
        "mwenda",
        "nnya",
        "satu",
        "sawa_meka",
        "sindika",
        "soma",
        "tandika",
        "tano",
        "tekako",
        "vaako",
        "yaka",
        "yongeza",
        "zeero",
        "zikira"
    ]
    _instance = None # to implement class as singleton
    
    def predict(self, file_path):
        #extract MFCCs
        MFCCs =self.preprocess(file_path)  #array shape(segments=44, coefficients =13)
        
        #convert 2D MFCCs array into 4D array >> (samples, segments=44, coefficients =13, channels =1)
        MFCCs = MFCCs[np.newaxis, ..., np.newaxis]
        
        #make prediction
        predictions = self.model.predict(MFCCs) 
        predicted_index = np.argmax(predictions)
        predicted_keyword = self._mappings[predicted_index]
        
        return predicted_keyword
    
        
    def preprocess(self, file_path, n_mfcc=13, n_fft=2048, hop_length=512):
       #load audio file
        signal, sr = librosa.load(file_path)
        
        #ensure consistency
        if len(signal) > NUM_SAMPLES_TO_CONSIDER:
            signal = signal [:NUM_SAMPLES_TO_CONSIDER]
            
        #extract MFCCs
        MFCCs = librosa.feature.mfcc(signal, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=hop_length)
        return MFCCs.T
    
    
def Keyword_Spotting_Service():
    #ensure only 1 instance of KwSS
    if _Keyword_Spotting_Service._instance is None:
        _Keyword_Spotting_Service._instance = _Keyword_Spotting_Service()
        _Keyword_Spotting_Service.model = keras.models.load_model(model_path)
    return _Keyword_Spotting_Service._instance  

if __name__ == "__main__":
    kss = Keyword_Spotting_Service()
    
    keyword2 = kss.predict("output.wav")
    
    print(f"Predicted keywords: {keyword2}")
    
    
    