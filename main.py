import discord
from discord import client
from discord.ext import commands
from Weather import Weather as WeatherStats
from Overwatch import Api
from Overwatch import UserStats
from decouple import config
from os import walk
from Models import *
from YTDLSource import YTDLSource

#api keys
DISOCRD_API_KEY = config('DISCORDBOTID', default=False)
WEATHER_API_KEY = config('XRAPIDAPIKEY', default=False)

#overwatch stats preference
checkInterval = 60
monitoringUsers = UserStats.monitoringUsers()

def getFiles():
    """
    Функция возвращает список файлов 
    """
    f = []
    for (dirpath, dirnames, filenames) in walk('.'):
        f.extend(filenames)
        break
    return f

def create_tables():
    """
    Функция создает базу данных
    """
    with database:
        database.create_tables([User])

class Overwatch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def startStats(self, ctx, battleNet):
        """
        Отслежование статистики
        """
        if UserStats.getUserById((ctx.author.id, 'discord')) == None:
            ovApi = Api('pc', 'global', battleNet.replace("#", "-"))
            if (str(ovApi.getUser()) == "{'message': 'Error: Profile not found'}"):
                await ctx.send("Игрок не найден")
            else:
                usr = UserStats(ctx.author.id, battleNet.replace("#", "-"), ovApi.getRanks(ovApi.getUser()))
                usr.addUser()
                await ctx.send('Аккаунт добавлен')
        else:
            await ctx.send('Аккаунт уже добавлен')


class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def weather(self, ctx):
        """Выводит погоду"""
        w = WeatherStats(WEATHER_API_KEY)
        weatherdata = w.parsData(w.getWeahter())
        icon = w.getWeatherIcon(weatherdata.get("icon"))
        w.card(weatherdata, icon)
        await ctx.send(file=discord.File('assets/tmp/currentWeather.png'))

description = '''Lina-Inverse'''
bot = commands.Bot(command_prefix='`', description=description)

@bot.event
async def on_ready():
    """Метод срабатывет при загрузке бота"""
    print('Logged in as ' + str(bot.user.name))
    if 'database.db' not in getFiles():
        create_tables()
    #bot playing in:
    await bot.change_presence(activity=discord.Game(name="`help"))
    
bot.add_cog(Weather(bot))
bot.add_cog(Overwatch(bot))
bot.run(DISOCRD_API_KEY)