"""
Создается БД, классы описывающие таблицы для хранения:
 1) данных о пользователе;
 2) данных об отеле;
 3) фотографий отеля.
Создаются таблицы БД.
"""

import datetime
from peewee import *
import os
from loguru import logger
from peewee import Database


abs_path = os.path.abspath(os.path.join('database', 'hotel_bot.db'))
db = SqliteDatabase(abs_path)  # Создаем БД (файл)


class BaseModel(Model):
    """
    Базовый класс для формирования всех наследуемых от него таблиц.
    Определяет, базу данных для всех наследуемых от него таблиц.
    """

    class Meta:
        """
        Вложенный класс, в котором происходит подключение к БД.
        При необходимости можно определить другие общие для таблиц параметры.

        Attributes:
            database (Database): устанавливает соединение с базой данных для базового класса.
        """

        database = db


class User(BaseModel):
    """
    Дочерний класс от родительского класса BaseModel. Определяет, поля таблицы users.

    Attributes:
        name (str): поле таблицы, в котором указывается имя пользователя.
        telegram_id (int): поле таблицы, в котором указывается id чата.
        command (str): поле таблицы, в котором указывается введенная пользователем команда.
        timestamp (datetime): поле таблицы, в которой указывается дата и время введения пользователем команды.
    """

    name = CharField()
    telegram_id = IntegerField()
    command = CharField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        """
        Вложенный класс, в котором указана БД.

        Attributes:
            order_by (str): автоматическая сортировка в таблице по полю telegram_id.
            db_table (str): устанавливает название таблицы.
        """

        order_by = 'telegram_id'
        db_table = 'users'  # название таблицы во множественном числе, чтобы
        # не путалось с полями (в единственном числе) и было сразу понятно к чему обращаемся


class Hotel(BaseModel):
    """
    Дочерний класс от родительского класса BaseModel. Определяет, поля таблицы hotels.

    Attributes:
            user (User): внешний ключ, связывает запись с объектом класса User.
            hotel (str): устанавливает название таблицы.
            address (str): устанавливает название таблицы.
    """

    user = ForeignKeyField(User, backref='hotels')  # название таблицы - hotels
    hotel = CharField()
    address = CharField()


class Image(BaseModel):
    """
    Дочерний класс от родительского класса BaseModel. Определяет, поля таблицы images.

    Attributes:
            hotel (Hotel): внешний ключ, связывает запись с объектом класса Hotel.
            image (str): ссылка на фото отеля.
    """
    hotel = ForeignKeyField(Hotel, backref='images')
    image = CharField()


with db:
    tables = [User, Hotel, Image]
    if not all(table.table_exists() for table in tables):
        db.create_tables(tables)  # создаем таблицы
        logger.debug('Таблицы созданы успешно.')
    else:
        logger.debug('Таблицы уже существуют.')
