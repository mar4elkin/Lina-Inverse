import asyncio
import discord
import json
from OverwatchWorker import OverwatchWorker
from ImageGen import ImageGen
import ast

class Stats(object):
    
    def __init__(self) -> None:
        pass

    @classmethod
    async def checkOverwatch(cls, bot):
        await bot.wait_until_ready()
        while True:
            for row in OverwatchWorker.getAllUsers():
                channel = bot.get_channel(int(row.channel))
                ovData = OverwatchWorker.getUserInfo(row.battleId)
                ovOldData = ast.literal_eval(row.overwatch_data)
                
                igen = ImageGen('overwatch', ovData, ovOldData)
                igen.drawImgOverwatch()
                await channel.send(file=discord.File('tmp/overwatch/overwatch.png'))
                
                if (ovData['games']['played'] > ovOldData['games']['played']):
                    if (ovData['ranks']['damage']['rank'] != ovOldData['ranks']['damage']['rank'] or ovData['ranks']['support']['rank'] != ovOldData['ranks']['support']['rank'] or ovData['ranks']['tank']['rank'] != ovOldData['ranks']['tank']['rank']):        
                        OverwatchWorker.updateUser(
                            str(row.battleId), 
                            str(ovData), 
                            str(ovOldData)
                        )
                        igen = ImageGen('overwatch', ovData, ovOldData)
                        await igen.drawImgOverwatch()
                        await channel.send(file=discord.File('tmp/overwatch/overwatch.png'))
                        #'tmp/overwatch/overwatch.png'
                        #await channel.send(str(row.overwatch_data))
            await asyncio.sleep(20)