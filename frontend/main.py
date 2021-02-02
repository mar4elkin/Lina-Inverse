import asyncio
import discord
from asyncio.tasks import sleep
from discord import client
from discord import channel
from discord.ext import commands
from decouple import config
from Models import *
from os import walk
from OverwatchWorker import OverwatchWorker
from Exceptions import EmptyString
from Exceptions import BattleTagAlready
from Stats import Stats


#api keys
DISOCRD_API_KEY = config('DISCORDBOTID', default=False)

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
        database.create_tables([UserOverwatch])

def dbCreater():
    if 'database.db' not in getFiles():
        print('База данных созданна')
        create_tables()
    
class Overwatch(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # @commands.command()
    # async def test(self, ctx):
    #     await ctx.send(discord.utils.get(ctx.guild.channels, name='land-of-bots').id)

    @commands.command()
    async def add_profile(self, ctx, battle_net=None): #, channel_name=None):
        """
        `add_profile user#1234
        Бот начинает отслеживать статистику.
        """
        channelId = ctx.channel.id

        if (battle_net is None):
            await ctx.send('Укажите battle tag')
        else:
            #channelId = discord.utils.get(ctx.guild.channels, name=channel_name).id
            battleId = battle_net
            if(OverwatchWorker.getUserByBattleTag(battleId) == []):
                ovData = OverwatchWorker.getUserInfo(battleId)
                empty_ranks = {
                        "games": {
                            "played": "0"
                        }, 
                        "player": {
                            "avatar": "", 
                            "nickname": "", 
                            "top_hero": ""
                        }, 
                        "ranks": {
                            "damage": {
                                "icon": "None", 
                                "rank": "None"
                            }, 
                            "support": {
                                "icon": "None", 
                                "rank": "None"
                            }, 
                            "tank": {
                                "icon": "None", 
                                "rank": "None"
                            }
                        }
                        }
                data = {
                    "discordId": str(ctx.author.id),
                    "battleId": str(battleId),
                    "channel": str(channelId),
                    "overwatch_data": str(ovData),
                    "overwatch_data_old_ranks": str(empty_ranks),
                    "check": True,
                }
                OverwatchWorker.addUser(data)
                await ctx.send("Аккаунт добавлен")
            else:
                await ctx.send("Данный аккаунт уже есть в базе")
    
description = '''Lina-Inverse'''
bot = commands.Bot(command_prefix='`', description=description)

@bot.event
async def on_ready():
    """
    Метод срабатывет при загрузке бота
    """
    print('Logged in as ' + str(bot.user.name))
    await bot.change_presence(activity=discord.Game(name="`help"))

dbCreater()
bot.loop.create_task(Stats.checkOverwatch(bot)) #, Stats.getAllUsers()))
bot.add_cog(Overwatch(bot))
bot.run(DISOCRD_API_KEY)