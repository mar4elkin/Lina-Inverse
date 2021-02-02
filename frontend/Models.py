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

class UserOverwatch(BaseModel):
    """
    Класс юзеров
    """
    Id = IntegerField(primary_key=True)
    discordId = CharField()
    battleId = CharField()
    overwatch_data = CharField()
    overwatch_data_old_ranks = CharField()
    check = BooleanField()
    channel = CharField()

class UserOsu(BaseModel):
    """
    Класс юзеров
    """
    Id = IntegerField(primary_key=True)
    discordId = IntegerField()
    ranks = CharField()