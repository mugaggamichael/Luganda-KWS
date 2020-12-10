from pydub import AudioSegment
import os # Needed for os.listdir

pad_ms = 1000

path = "tee"

for filename in os.listdir(path): # Loop over all items in the path
    if (filename.endswith(".wav")): # Check if the file ends with .wav
        audio = AudioSegment.from_wav(filename)
        assert pad_ms > len(audio), + str(full_path)
        silence = AudioSegment.silent(duration=pad_ms-len(audio)+1)

        padded = audio + silence

        newFilename = filename.split(".")[0] + "_1.wav" # And something like this for the new name
        padded.export(newFilename, format='wav')