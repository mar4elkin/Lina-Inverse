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

# class Queue(BaseModel):
#     """
#     Класс очереди для песен
#     """
#     Id = IntegerField(primary_key=True)
#     songName = CharField()
