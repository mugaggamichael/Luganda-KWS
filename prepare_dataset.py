#MFCC
import librosa #audio library
import os #manipulate files
import json #create json files

DATASET_PATH = "dataset"
JSON_PATH = "data.json"
SAMPLES_TO_CONSIDER = 22050 #1 second worth of sound basing on librosa's 

#go through audio files, extract mfcc, save it in json file
def prepare_dataset(DATASET_PATH, JSON_PATH, n_mfcc=13, hop_length=512, n_fft=2048):
    #data dictionary to store all info from audio
    data = {
        "mappings":[],
        "labels":[],
        "MFCCs":[],
        "files":[]
    }
    #loop through all sub-dirs
    for i, (dirpath, dirnames, filenames) in enumerate(os.walk(DATASET_PATH)):
        #ensure we are not at root level
        if dirpath is not DATASET_PATH:
            #update mappings
            category =dirpath.split("/")[-1]
            data["mappings"].append(category)
            print(f"processing{category}")
            
            #loop through all filenames and extract mfcc
            for f in filenames:
                #get file path
                file_path = os.path.join(dirpath, f)
                #load audio file
                signal, sr = librosa.load(file_path)
                #ensure the audio file is atleast 1 sec
                if len(signal) >= SAMPLES_TO_CONSIDER:
                    #enforce 1 sec long signal
                    signal = signal [:SAMPLES_TO_CONSIDER]
                    
                    #extract MFCCs
                    MFCCs = librosa.feature.mfcc(signal, n_mfcc=n_mfcc, hop_length=hop_length, n_fft=n_fft)
                    
                    #store data
                    data["labels"].append(i-1)
                    data["MFCCs"].append(MFCCs.T.tolist())
                    data["files"].append(file_path)
                    print(f'{file_path}:{i-1}')
      
    #store in json file
    with open(JSON_PATH, "w") as fp:
        json.dump(data, fp, indent=4)
        
if __name__ == "__main__":
    prepare_dataset(DATASET_PATH, JSON_PATH)