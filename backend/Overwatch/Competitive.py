from os import stat
from typing import List
from bs4 import BeautifulSoup
import requests
#from .Exceptions import BattleTagError

class Competitive(object):
    """
    Класс для получения рейтинговых очков и игр
    """
    def __init__(self, battle_tag) -> None:
        """
        Конструктор на вход требуется battle tag 
        """
        self.url = f"https://playoverwatch.com/en-us/career/pc/{battle_tag}"
    
    
    def getPage(self) -> BeautifulSoup:
        """
        Получение страницы
        """
        page = requests.get(self.url)
        if (page.status_code == 200):
            return BeautifulSoup(page.text, "html.parser")
    
    def playerInfo(self, page: BeautifulSoup) -> dict:
        """
        Информация об игроке авотра и ник
        """
        return { 
                'avatar': page.find('img', 'player-portrait')['src'], 
                'nickname': page.find('h1', 'header-masthead').text,
                'top_hero': page.find('div', 'masthead-hero-image')['style'].split('background-image:')[1].replace(' ', '')
                }
    
    def getGames(self, page: BeautifulSoup) -> dict:
        """
        Поиск сыгранных игр в соревновательном режиме
        """
        stats = {}
        # господи ура 

        stats['played'] = page.select_one('.masthead-detail > span:nth-child(1)').text.split(' ')[0]
        
        # compStats = page.select_one('#competitive > section:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(4) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(2)').find_all('td')
        # for index in range(1, len(compStats)):
        #     if (index % 2 == 0):
        #         stats[compStats[index].text] = compStats[index + 1].text
        #     else:
        #         stats[compStats[0].text] = compStats[1].text

        return stats
    
    def getRanks(self, page: BeautifulSoup) -> dict:
        """
        Поиск рейтинговых очков
        """
        
        ovranks = {}
        tank = {}
        damage = {}
        support = {}

        ranks = page.select('div.competitive-rank-section')

        if (len(ranks) == 6*2):
            ranks = ranks[:-3*2]
        elif (len(ranks) == 4*2):
            ranks = ranks[:-2*2]
        elif (len(ranks) == 2*2):
            ranks = ranks[:-1*2]

        for rank in ranks:
            try:
                if (rank.find('div', 'competitive-rank-tier')['data-ow-tooltip-text'] == 'Tank Skill Rating'):
                    try:
                       tank["rank"] = rank.find('div', class_='competitive-rank-level').text
                    except AttributeError:
                        tank["rank"] = "None"
                    
                    try:
                        tank["icon"] = rank.find('img', class_='competitive-rank-tier-icon')['src']
                    except AttributeError:
                        tank["icon"] = "None"

            except TypeError:
                tank["rank"] = "None"
                tank["icon"] = "None"

            try:
                if (rank.find('div', 'competitive-rank-tier')['data-ow-tooltip-text'] == 'Damage Skill Rating'):
                    try:
                       damage["rank"] = rank.find('div', class_='competitive-rank-level').text
                    except AttributeError:
                        damage["rank"] = "None"
                    
                    try:
                        damage["icon"] = rank.find('img', class_='competitive-rank-tier-icon')['src']
                    except AttributeError:
                        damage["icon"] = "None"
            except TypeError:
                damage["rank"] = "None"
                damage["icon"] = "None"

            try:
                if (rank.find('div', 'competitive-rank-tier')['data-ow-tooltip-text'] == 'Support Skill Rating'):
                    try:
                       support["rank"] = rank.find('div', class_='competitive-rank-level').text
                    except AttributeError:
                        support["rank"] = "None"
                    
                    try:
                        support["icon"] = rank.find('img', class_='competitive-rank-tier-icon')['src']
                    except AttributeError:
                        support["icon"] = "None"
            except TypeError:
                support["rank"] = "None"
                support["icon"] = "None"
    

        ovranks['tank'] = tank
        ovranks['damage'] = damage
        ovranks['support'] = support

        return ovranks

    def checkPage(self, page: BeautifulSoup) -> None:
        """
        Проверка страницы на наличие информации
        """
        if (page.title.string == 'Overwatch'):
            raise BattleTagError(self.url)
        

