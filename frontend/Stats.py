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
                if (ovData['games']['played'] > ovOldData['games']['played']):
                    blogger(f"games new {ovData['games']['played']} and old {ovOldData['games']['played']}")
                    if (ovData['ranks']['damage']['rank'] != ovOldData['ranks']['damage']['rank'] or ovData['ranks']['support']['rank'] != ovOldData['ranks']['support']['rank'] or ovData['ranks']['tank']['rank'] != ovOldData['ranks']['tank']['rank']):        
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
                        await channel.send(file=discord.File('tmp/overwatch/overwatch.png'))
                        #'tmp/overwatch/overwatch.png'
                        #await channel.send(str(row.overwatch_data))
                    else:
                        blogger(f"if did't works ranks new {ovData['ranks']} and old {ovOldData['ranks']}")
            await asyncio.sleep(1200)