import speech_recognition as sr 
import warnings
warnings.filterwarnings("ignore")

def listen():
    r = sr.Recognizer()
                                                                 
    with sr.Microphone() as source:
        print("Don't say anything adjusting to background noises")
        r.adjust_for_ambient_noise(source, duration = 1)                                                                            
        print("Listening for your Command:")                                                                                
        audio = r.listen(source , 3 , 4)   
    try:
        print("You said " + r.recognize_google(audio))
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
