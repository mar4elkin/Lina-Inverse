import asyncio
import discord
import json
from OverwatchWorker import OverwatchWorker
from ImageGen import ImageGen
import ast
from Logger import blogger

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
                blogger(f"Checking rows in Stats.py ovData: {ovData} ovOldData {ovOldData} for user {row.battleId}")
                if (ovOldData['ranks']['damage'] != {} and ovData['ranks']['damage'] != {}):
                    if (ovData['ranks']['damage'] != {} and ovOldData['ranks']['damage'] == {}):
                        blogger(f"games new {ovData['games']['played']} and old {ovOldData['games']['played']}")
                        blogger(f"ranks dd new {ovData['ranks']['damage']['rank']} and old {ovOldData['ranks']['damage']['rank']}")
                        blogger(f"ranks support new {ovData['ranks']['support']['rank']} and old {ovOldData['ranks']['support']['rank']}")
                        blogger(f"ranks tank new {ovData['ranks']['tank']['rank']} and old {ovOldData['ranks']['tank']['rank']}")
                        OverwatchWorker.updateUser(
                            str(row.battleId), 
                            str(ovData), 
                            str(ovOldData)
                        )
                        igen = ImageGen('overwatch', ovData, ovOldData)
                        igen.drawImgOverwatch()
                        blogger(f"message sended")
                        await channel.send(f'<@!{row.discordId}>', file=discord.File('tmp/overwatch/overwatch.png'))
                    
                    elif (ovData['games']['played'] > ovOldData['games']['played']):
                        blogger(f"games new {ovData['games']['played']} and old {ovOldData['games']['played']}")
                        blogger(f"ranks dd new {ovData['ranks']['damage']['rank']} and old {ovOldData['ranks']['damage']['rank']}")
                        blogger(f"ranks support new {ovData['ranks']['support']['rank']} and old {ovOldData['ranks']['support']['rank']}")
                        blogger(f"ranks tank new {ovData['ranks']['tank']['rank']} and old {ovOldData['ranks']['tank']['rank']}")
                        OverwatchWorker.updateUser(
                            str(row.battleId), 
                            str(ovData), 
                            str(ovOldData)
                        )
                        igen = ImageGen('overwatch', ovData, ovOldData)
                        igen.drawImgOverwatch()
                        blogger(f"message sended")
                        await channel.send(f'<@!{row.discordId}>', file=discord.File('tmp/overwatch/overwatch.png'))
                        #'tmp/overwatch/overwatch.png'
                        #await channel.send(str(row.overwatch_data))
                await asyncio.sleep(1200)