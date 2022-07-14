from __future__ import unicode_literals
import youtube_dl
import os
import subprocess
from os import path
from pydub import AudioSegment
import speech_recognition as sr 
from pydub.silence import split_on_silence


# poster

def poster():
    a = """
    
    
                '##:::'##:'########::'######::'##::::'##:'##::::'##:
                . ##:'##::... ##..::'##... ##: ##:::: ##: ###::'###:
    	        :. ####:::::: ##:::: ##:::..:: ##:::: ##: ####'####:
	        ::. ##::::::: ##::::. ######:: ##:::: ##: ## ### ##:
	        ::: ##::::::: ##:::::..... ##: ##:::: ##: ##. #: ##:
	        ::: ##::::::: ##::::'##::: ##: ##:::: ##: ##:.:: ##:
	        ::: ##::::::: ##::::. ######::. #######:: ##:::: ##:
	        :::..::::::::..::::::......::::.......:::..:::::..::  
	                                                            
	                                                           (A YouTube video Summariser)
	                                                         
	                                                     by 
	                                                        Jeevan Raj SR
	                                                        Adil Afnan VK
	                                                        Akarsh K
	                                                        Anfas KP
	   
	   
	   
	        """
    print(a)


# yt video to audio download

subprocess.call('clear')
poster()

print("Insert the link: ", end = " ")
link = input ("")

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],'outtmpl': 'ytaud.mp3'
}

print("\n \033[1m Downloading the Audio of the YouTube file... \033[0m ")
print('\n')

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([link])
        
    
# audio mp3 to wav
 
print("\n  \033[1m  Wait a sec....Converting audio formats! \033[0m ")
print('\n')

subprocess.call(['ffmpeg', '-i', 'ytaud.mp3','yt.wav'])

subprocess.call('clear')
poster()

dst = "yt.wav"

print("Transcribing....")
# audio to text

r = sr.Recognizer()

def get_audio_transcription(path):
    sound = AudioSegment.from_wav(path)  
    chunks = split_on_silence(sound,min_silence_len = 500,silence_thresh = sound.dBFS-14,keep_silence=500,)
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
                print("Transcribing....", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    with open("sum.txt", "w") as f:
        f.write(whole_text)
        f.close()
    return whole_text 

if __name__ == '__main__':
    import sys
    path = dst
    print("Transcribing....")
    print("\nFull text:", get_audio_transcription(path))
    subprocess.call('clear')
    poster()
    print('\n The YouTube video has been successfully summarised and you can access it from the "sum.txt" file.')
    
    
    
    
    
    
    
