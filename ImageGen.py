from PIL import Image, ImageDraw, ImageFilter, ImageFont

class ImageGen(object):
    """
    Класс для работы с изображениями
    """
    def __init__(self, weatherData):
        """
        Конструктор weatherData обязательный параметр 
        """
        self.body = 'assets/background.png'
        self.wIcon = 'assets/tmp/weather.png'
        self.weatherData = weatherData

    def cardHolder(self):
        """
        Метод для генерации карточки используется переменные из конструктора в которых храниться путь к картинкам
        """
        #init images
        body = Image.open(self.body)
        icon = Image.open(self.wIcon)
        #paste weather icon to body image
        body.paste(icon, (0, 40), icon)
        #enable body drawing 
        draw = ImageDraw.Draw(body)
        #temp
        font = ImageFont.truetype("NotoSansMono-Light.ttf", 26)
        draw.text((95, 55), self.weatherData.get("temp") + "°C",(255,255,255), font=font)
        #temp_feels
        font = ImageFont.truetype("NotoSansMono-Light.ttf", 16)
        draw.text((95, 85), "Ощущается как: " + self.weatherData.get("feels_like") + "°C",(255,255,255), font=font)
        #city
        font = ImageFont.truetype("NotoSansMono-Light.ttf", 22)
        draw.text((20, 20), self.weatherData.get("city"),(255,255,255), font=font)
        #windspeed
        font = ImageFont.truetype("NotoSansMono-Light.ttf", 16)
        draw.text((95, 105), "Скорость ветра: " + self.weatherData.get("wind_speed") + "m/s",(255,255,255), font=font)
        #description
        font = ImageFont.truetype("NotoSansMono-Light.ttf", 16)
        draw.text((95, 125), self.weatherData.get("description"),(255,255,255), font=font)
        #commit
        body.save('assets/tmp/currentWeather.png', quality=95)