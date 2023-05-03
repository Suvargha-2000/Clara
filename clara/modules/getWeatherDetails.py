import requests , json
from datetime import date
import config
import time 

def getWeatherData(debug=False) :
    if config.debug:
        time.sleep(2)
        return "Testing"
    
    with open("links/others.json" , "r") as file3 :
        other_data = json.load(file3)
        file3.close()

    if other_data["weather_date"] == str(date.today()):
        weather_forecast = other_data["weather_value"]
    else :
        #this api key should be made from the website 
        api_key = None
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = 'Agarpāra, IN'
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
        response = requests.get(complete_url) 
        x = response.json() 
        y = x["main"] 
        current_temperature = y["temp"] 
        current_pressure = y["pressure"] 
        current_humidiy = y["humidity"] 

        z = x["weather"] 

        weather_description = z[0]["description"] 
        
        weather_forecast = ((" Temperature is") +
                    str(format((float(current_temperature)-273.15) , ".2f"))+'degree celsius' + 
            "\n atmospheric pressure is " +
                    str(current_pressure)+'hPa' +
            "\n humidity is " +
                    str(current_humidiy))
        data = {
            "weather_date" : str(date.today) ,
            "weather_value" : weather_forecast
        }


        with open("links/others.json" , "w") as file4:
            json.dump(data ,  file4)
        
    return weather_forecast