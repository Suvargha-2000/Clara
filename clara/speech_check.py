import speech_recognition as sr 
import winsound
import pygame
# import pyttsx3  
from playsound import playsound
import os
from gtts import gTTS
import requests
import json 
# *****************AI************
import nltk 
from nltk.stem import LancasterStemmer
import numpy as np
import tflearn
import serial
import time
import random
from datetime import date

# import pickle
stemmer = LancasterStemmer()
serial_com = False
nltk.download('punkt')

serial_text = 'none'
serial_text_before = ''
# ***********AI 
with open('training_data/training.json') as file:
    data = json.load(file)


words = []
labels = []
docs_x = []
docs_y = []

for intent in data['intents'] :
    for pattern in intent['patterns'] :
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent['tag'])

    if intent['tag'] not in labels:
        labels.append(intent['tag'])


words = [stemmer.stem(w.lower()) for w in words if w not in ['?' , '!']]
words = sorted(list(set(words)))
labels = sorted(labels)

training = []
output = []

out_empty = [ 0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []

    wrds = [stemmer.stem(w.lower()) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)


training = np.array(training)
output = np.array(output)


net = tflearn.input_data(shape = [None , len(training[0])])
net = tflearn.fully_connected(net , 8)
net = tflearn.fully_connected(net , 8)
net = tflearn.fully_connected(net , len(output[0]) , activation= 'softmax')
net = tflearn.regression(net)
model = tflearn.DNN(net)
model.fit(training , output , n_epoch=1000 , show_metric= True)

def bag_of_words(s , words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(w.lower()) for w in s_words]
    
    for se in s_words:
        for i , w in enumerate(words):
            if w == se :
                bag[i]  = 1

    return np.array(bag)

# ******AI *****************

def speak(text):
    tts = gTTS(text=text, lang='en-uk')
    try: 
        pygame.quit()
        os.remove('voice.mp3')
        filename = 'voice.mp3'
        tts.save(filename)
        # playsound(filename)
        # winsound.PlaySound(filename, winsound.SND_FILENAME)
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

    except: 
        filename = 'voice.mp3'
        tts.save(filename)
        # playsound(filename)
        # winsound.PlaySound(filename, winsound.SND_FILENAME)
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
    



# ******serial communication
serial_com = False
try :
    ser = serial.Serial('COM3', 9600)
    ser.flushInput()
    password_return = 0
    print('Working Live')
    working = True
    while working :
        ser_bytes = ser.readline()
        decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        if decoded_bytes == '123456':
            password_return = 1
            speak('Password Matched')
            serial_com = True
            working = False
        else :
            speak('Please give the correct password!')

except:
    speak('serial Com not available, going to direct input')
# ********serial end




def call_ai(text):
    inpt = text 
    predict = np.argmax(model.predict([bag_of_words(inpt , words)]))
    print(labels[predict])
    commands(labels[predict] , text)


# with open("links/others.json" , "r") as file3 :
#     other_data = json.load(file3)
#     file3.close()

# if other_data["weather_date"] == str(date.today()):
#     weather_forecast = other_data["weather_value"]
# else :
#     api_key = "dc6cb0be2473488e7d34536f64d97996"
#     base_url = "http://api.openweathermap.org/data/2.5/weather?"
#     city_name = 'Agarpāra, IN'
#     complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
#     response = requests.get(complete_url) 
#     x = response.json() 
#     y = x["main"] 
#     current_temperature = y["temp"] 
#     current_pressure = y["pressure"] 
#     current_humidiy = y["humidity"] 

#     z = x["weather"] 

#     weather_description = z[0]["description"] 
    
#     weather_forecast = ((" Temperature is") +
#                 str(format((float(current_temperature)-273.15) , ".2f"))+'degree celsius' + 
#         "\n atmospheric pressure is " +
#                 str(current_pressure)+'hPa' +
#         "\n humidity is " +
#                 str(current_humidiy))
#     data = {
#         "weather_date" : str(date.today) ,
#         "weather_value" : weather_forecast
#     }


#     with open("links/others.json" , "w") as file4:
#         json.dump(data ,  file4)




weather_forecast = 'now we are testing . weather api is used for final purpose'



r = sr.Recognizer()  
x = 1
# songs as per user choice
with open("links/songs.json") as file2:
    songs_data = json.load(file2)


def commands(text , given_text):
    if 'gmail' in text:
        print('opening gmail')
        speak('opening gmail for the account suvargha2000')
        file = "https://mail.google.com/mail/u/1/#inbox"
        os.system("start brave "+file)
    elif 'facebook' in text:
        print('opening facebook')
        speak('opening facebook sir')
        file = 'https://www.facebook.com/'
        os.system("start brave "+file)
    elif 'good_morning' in text:
        print('Home process starts')
        file = "C:/Users/suvar/Downloads/song.mp3"
        os.system(file)
        speak('Good morning sir. Sara at your service .' + weather_forecast)
    elif 'song' in text:
        speak('here is a song you like')
        genres = []
        chooseable_songs = []
        for i in range(8):
            genres.append(songs_data[i]["genre"])
            if songs_data[i]["genre"] in given_text:
                chooseable_songs.append(i)
        if len(chooseable_songs) != 0 :
            song_index = random.choice(chooseable_songs)
        else :
            song_index = random.randint(0,8)
        speak(songs_data[song_index]["name"])
        file = songs_data[song_index]["link"]
        os.system("start brave "+file)
    elif 'weather' in text:
        print('weather')
        speak('Weather at your home is ' + weather_forecast)
        if 'rainy' in weather_forecast:
            speak('sir ! I will also advise you to take an umbrella.')
    elif 'whatsapp' in text:
        speak('Right Away Sir!')
        file = 'https://web.whatsapp.com/'
        os.system("start brave "+file)
    elif 'sleep' in text:
        speak('Going to sleep sir. Clara will be at you service.')
    else :
        speak('Just a minute sir')

    

with sr.Microphone() as source2: 
        
    r.adjust_for_ambient_noise(source2, duration=0.02)
    while x != 0 : 
        print('listening.....')
        if serial_com :
            # ser = serial.Serial('COM3', 9600)
            ser.flushInput()
            ser_bytes = ser.readline()
            if serial_text != 'none':
                serial_text_before = serial_text
            serial_text = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            if serial_text_before == serial_text and (serial_text == 'system make_noise' or serial_text=="song"):
                speak('Already a song is running sir')
                serial_text = 'avoid'
            if 'exit' in serial_text:
                x = 0
            elif 'avoid' in serial_text:
                serial_text = 'system make_noise'
            else:
                print(serial_text)
                call_ai(serial_text)
        else :
            try :
                audio2 = r.listen(source2 , phrase_time_limit= 4.5 , timeout=7) 
                MyText = r.recognize_google(audio2) 
                MyText = MyText.lower()
                if 'exit' in MyText:
                    x = 0
                else:
                    print(MyText)
                    call_ai(MyText)
            except:
                pass
