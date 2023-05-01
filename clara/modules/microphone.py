from gtts import gTTS
from playsound import playsound
import os
def microphoneCom(voice) :
    language = 'en'
    myobj = gTTS(text=voice, lang=language, slow=False)
    myobj.save("welcome.mp3")
    playsound('welcome.mp3')
    os.remove("welcome.mp3")
