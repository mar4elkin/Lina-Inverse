import discord
from discord.ext import commands
from Weather import Weather
from decouple import config
from os import walk
import os
import asyncio
from Models import *
from YTDLSource import YTDLSource

DISOCRD_API_KEY = config('DISCORDBOTID', default=False)
WEATHER_API_KEY = config('XRAPIDAPIKEY', default=False)


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
        database.create_tables([])

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, *, url):
        """Запускает адскую машину для гачи база"""
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player)
        await ctx.send('Сейчас играет: {}'.format(player.title))


    @commands.command()
    async def stop(self, ctx):
        """Я устал, я ухожу"""
        await ctx.voice_client.disconnect()

    
    @commands.command()
    async def skip(self, ctx):
        """Скипаем гачи..."""
        ctx.voice_client.stop()
        await ctx.send("Песня скипнута")

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("Зайди в канал БАКА")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            # нужно нормально сделать очередь !!!!!!!!
            await ctx.send("Добавленно в очередь")
            while (True):
                await asyncio.sleep(1)
                if ctx.voice_client.is_playing() == True:
                    continue
                else:
                    break
            #ctx.voice_client.stop()


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

@bot.command()
async def weather(ctx):
    """Выводит погоду"""
    w = Weather(WEATHER_API_KEY)
    weatherdata = w.parsData(w.getWeahter())
    icon = w.getWeatherIcon(weatherdata.get("icon"))
    w.card(weatherdata, icon)
    await ctx.send(file=discord.File('assets/tmp/currentWeather.png'))

bot.add_cog(Music(bot))
bot.run(DISOCRD_API_KEY)