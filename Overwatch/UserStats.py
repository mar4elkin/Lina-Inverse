import asyncio
from Models import *

class UserStats():
    """
    Класс для работы со статистикой пользователей
    """
    def __init__(self, discordUserId: str, battleNetId: str, lastRank: dict) -> None:
        self.discordUserId = discordUserId
        self.battleNetId = battleNetId
        self.lastRank = lastRank

    @classmethod
    def monitoringUsers(cls) -> list:
        """
        Метод для поиска проверяемых юзеров
        """
        query = User.select()
        users = []
        
        for row in query:
            #id battlenet monitor 
            if (row.monitor == True):
                users.append([row.Id, row.battleNetId, row.monitor])

        return users
    
    @classmethod
    def getUserById(cls, ids: tuple) -> int:
        """
        Метод для получения пользователя по id (discord/battlenet/db_id)
        """

        def getUser(idv, idType):
            query = ''
            userId = ''

            if (idType == 'discord'):
                query = User.select(User.Id).where(User.discordUserId == idv)
            elif(idType == 'battlenet'):
                query = User.select(User.Id).where(User.battleNetId == idv)
            elif(idType == 'db_id'):
                query = User.select(User.Id).where(User.Id == idv)

            for row in query: 
                userId = row
            
            if (userId == ''):
                userId = None
            
            return userId

        userId = ''
        idText = ''
        idType = ''

        try:
            idText = ids[0]
            idType = ids[1]
        except IndexError:
            print('Id must be tuple')
        
        if (idText != '' and idType != ''):
            if (idType == 'discord' or idType == 'battlenet' or idType == 'db_id'):
                userId = getUser(idText, idType)
            else:
                print('Check your idType!') 
        
        return userId            

    def addUser(self) -> None:
        User.create(
            discordUserId = self.discordUserId,
            battleNetId = self.battleNetId,
            lastRank = self.lastRank,
            monitor = 'True'
        )

        


