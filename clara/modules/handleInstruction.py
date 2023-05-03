import subprocess , json , random
from . import getWeatherDetails , voice
class handleInstructions : 
    def __init__(self) -> None:
        pass

    def startProcess(self , command : str , voiceInput : str) -> None :
        if "control" in voiceInput : 
            pass 
        elif command == "song":
            self.__songOpener()

        elif command in ["gmail" , "facebook" , "whatsapp"]:
            self.__handleApplication(command)

        elif command == "weather" :
            weather = getWeatherDetails.getWeatherData()
            voice.say(weather)
        
        elif command == "sleep" :
            pass 
        else :
            pass 
    
    def __handleApplication(self , command) -> None : 
        print(command)
        pass

    def __songOpener(self) -> None :
        jsonFile = json.load(open("clara/links/songs.json" , "r"))
        songs = [i for i in jsonFile]
        choosen = songs[random.randint(0 , len(songs))] 
        voice.say(choosen['name'] + "of Genre " + choosen["genre"])
        subprocess.Popen(["chromium-browser" , choosen["link"]])
