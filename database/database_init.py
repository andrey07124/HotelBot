import datetime
from peewee import *
import os
from loguru import logger


abs_path = os.path.abspath(os.path.join('database', 'hotel_bot.db'))
db = SqliteDatabase(abs_path)  # Создаем БД (файл)


class BaseModel(Model):
    """Базовый класс. Определяет, базу данных для всех наследуемых от него таблиц"""
    class Meta:
        database = db


class User(BaseModel):
    """Дочерний класс. Определяет, поля таблицы users"""
    name = CharField()
    telegram_id = IntegerField()
    command = CharField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        order_by = 'telegram_id'  # автоматическая сортировка в таблице по полю telegram_id
        db_table = 'users'  # чтобы название таблицы было во множественном числе,
        # не путалось с полями (в единственном числе) и было сразу понятно к чему обращаемся


class Hotel(BaseModel):
    """Дочерний класс. Определяет, поля таблицы hotels"""
    user = ForeignKeyField(User, backref='hotels')  # название таблицы - hotels
    hotel = CharField()
    address = CharField()


class Image(BaseModel):
    """Дочерний класс. Определяет, поля таблицы images"""
    hotel = ForeignKeyField(Hotel, backref='images')
    image = CharField()  # ссылки на фото


with db:
    tables = [User, Hotel, Image]
    if not all(table.table_exists() for table in tables):
        db.create_tables(tables)  # создаем таблицы
        logger.debug('Таблицы созданы успешно.')
    else:
        logger.debug('Таблицы уже существуют.')

