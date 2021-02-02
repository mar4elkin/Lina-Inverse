import discord
import requests
from Models import *
from decouple import config

class OverwatchWorker(object):
    def __init__(self):
        pass

    @staticmethod
    def getAllUsers() -> list:
        users = []
        for user in UserOverwatch.select().where(UserOverwatch.check == True):
            users.append(user)
        return users
    
    @staticmethod
    def getUserByBattleTag(tag) -> list:
        users = []
        for user in UserOverwatch.select().where(UserOverwatch.battleId == tag):
            users.append(user)
        return users
    
    @staticmethod
    def addUser(userData: dict) -> None:
        if (OverwatchWorker.getUserByBattleTag(userData['battleId']) == []):
            UserOverwatch.insert(
                discordId = userData['discordId'],
                battleId = userData['battleId'],
                overwatch_data = userData['overwatch_data'],
                overwatch_data_old_ranks = userData['overwatch_data_old_ranks'],
                check = True,
                channel = userData['channel']
            ).execute()
    
    @staticmethod
    def delUser(cls) -> None:
        pass

    @staticmethod
    def giveBackUser(cls) -> None:
        pass

    @staticmethod
    def updateUser(battleId: str, overwatch_data: dict, overwatch_old_data: dict) -> None:
        UserOverwatch.update(
            overwatch_data = overwatch_data,
            overwatch_data_old_ranks = overwatch_old_data
        ).where(UserOverwatch.battleId == battleId)

    @staticmethod
    def getUserInfo(battletag: str) -> str:
        return requests.get(f"{config('BACKEND_URL', default=False)}{battletag.replace('#', '-')}").json()
