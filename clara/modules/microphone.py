from gtts import gTTS
from playsound import playsound
import os

def microphoneCom(voice) :
    language = 'en'
    myobj = gTTS(text=voice, lang=language, slow=False)
    myobj.save("voice.mp3")
    playsound('voice.mp3')
    os.remove("voice.mp3")
