import requests
from ImageGen import ImageGen
import json 

class Weather(object):
    """
    Класс для получения мето данных через open-weather api
    """
    def __init__(self, xRapidapiKey, cityName="Saint Petersburg,ru"):
        """
        Конструктор cityName не обязательный параметр. xRapidapiKey - api ключ, хранится в env
        """
        self.city = cityName
        self.xRapidapiKey = xRapidapiKey
    
    def getWeahter(self):
        """
        Метод для получения данных от api 
        """
        url = "https://community-open-weather-map.p.rapidapi.com/weather"
        querystring = {
            "q": self.city, 
            "lang": "ru",
            "units": "metric"
            }
        headers = {
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
            'x-rapidapi-key': self.xRapidapiKey
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        return response.text

    def parsData(self, weatherData):
        """
        Метод извлекает данные из json строки и создает объект с нужными для рендера данными
        """
        weatherDict = json.loads(weatherData)
        weatherObject = {
            "temp": str(int(weatherDict.get("main")["temp"])),
            "description": str(weatherDict.get("weather")[0].get("description")),
            "feels_like": str(int(weatherDict.get("main").get("feels_like"))),
            "wind_speed": str(weatherDict.get("wind").get("speed")),
            "icon": str(weatherDict.get("weather")[0].get("icon")),
            "city": str(weatherDict.get("name"))
        }
        return weatherObject
    
    def getWeatherIcon(self, iconId, zoom="2x"):
        """
        Метод возвращает ссылку на иконку 
        """
        url = "http://openweathermap.org/img/wn/" + iconId + "@" + zoom + ".png"
        return url

    def card(self, weatherData, imageUrl):
        """
        Метод для генерации карточки с погодой
        """
        img_data = requests.get(imageUrl).content
        with open('assets/tmp/weather.png', 'wb') as handler:
            handler.write(img_data)
        imageGen = ImageGen(weatherData)
        imageGen.cardHolder()
