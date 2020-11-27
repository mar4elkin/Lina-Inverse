from peewee import *

DATABASE = 'database.db'

database = SqliteDatabase(DATABASE)

class BaseModel(Model):
    """
    Класс моделей базы данных
    """
    class Meta:
        """
        Мета класс для работы peewee
        """
        database = database

class User(BaseModel):
    """
    Класс юзеров
    """
    Id = IntegerField(primary_key=True)
    discordUserId = IntegerField()
    battleNetId = CharField()
    lastRank = CharField()
    monitor = BooleanField()

