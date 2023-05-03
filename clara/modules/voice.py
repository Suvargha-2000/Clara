from gtts import gTTS
from playsound import playsound
import os

def say(voice) :
    language = 'en'
    myobj = gTTS(text=voice, lang=language, slow=False)
    myobj.save(f'{voice}.mp3')
    playsound(f'{voice}.mp3')
    os.remove(f'{voice}.mp3')
