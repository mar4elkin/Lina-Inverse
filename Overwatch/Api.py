import requests

class Api():
    """
    Класс для работы с api overwatch
    """

    def __init__(self, platform, region, user) -> None:
        self.url = "https://owapi.io/profile/" + platform + "/" + region + "/" + user

    def getUser(self):
        """
        Метод для получение юзера
        """
        return requests.get(self.url).json()

    def getRanks(self, data):
        """
        Метод для получение ранков юзера
        """
        return data['competitive']