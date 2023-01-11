"""Прописаны функции, для работы с таблицами БД."""
import peewee
import select

from database.database_init import db, User, Hotel, Image
from peewee import *
from loguru import logger
from typing import List  # для аннотации
from peewee import ModelSelect  # для аннотации


@logger.catch
def table_users_filling(name: str, telegram_id: int, command: str) -> User:
    """
    Заполнение таблицы users.

    :param name: имя пользователя.
    :type name: str.
    :param telegram_id: id чата.
    :type telegram_id: int.
    :param command: команда, введенная пользователем.
    :type command: str.
    :return: user: запись в таблице users.
    :rtype: user: User
    """

    command_selection = {'PRICE_LOW_TO_HIGH': '/lowprice',
                         'PRICE_HIGH_TO_LOW': '/highprice',
                         'DISTANCE': '/bestdeal'}
    with db:
        user = User.create(name=name, telegram_id=telegram_id, command=command_selection[command])
    logger.debug('Внесена запись в таблицу users')
    return user


@logger.catch
def table_hotels_filling(user: User, hotel: str, address: str) -> Hotel:
    """
    Заполнение таблицы hotels.

    :param user: запись в таблице users.
    :type user: User.
    :param hotel: название отеля.
    :type hotel: str.
    :param address: адрес отеля.
    :type address: str.
    :return: hotel_bd: запись в таблице hotels.
    :rtype: hotel_bd: Hotel.
    """

    with db:
        hotel_bd = Hotel.create(user=user, hotel=hotel, address=address)
        logger.debug('Внесена запись в таблицу hotels')
    return hotel_bd


@logger.catch
def table_images_filling(hotel: Hotel, image: str) -> None:
    """
    Заполнение таблицы images.

    :param hotel: запись в таблице hotels.
    :type hotel: Hotel.
    :param image: ссылка на фото отеля.
    :type image: str.
    :return: None.
    """

    with db:
        Image.create(hotel=hotel, image=image)
        logger.debug('Внесена запись в таблицу images')


@logger.catch
def table_users_output(telegram_id: int) -> peewee.ModelSelect:  # TODO не уверен что верно описал тип вывода.
    """
    Функция, передающая для вывода историю таблицы users.

    :param telegram_id: id чата.
    :type telegram_id: int.
    :return: query: 5 последних записей истории из БД.
    :rtype: query: peewee.ModelSelect.
    """

    with db:
        # отбираем для вывода 5 последних записей истории из БД
        query = User.select().where(User.telegram_id == telegram_id).limit(5).order_by(User.id.desc())
        logger.debug('Отобраны запросы для вывода истории.')
    return query


@logger.catch
def table_images_output(hotel_db: Hotel) -> List[str]:
    """
    Функция, передающая для вывода историю таблицы images.

    :param hotel_db: запись в таблице hotels.
    :type hotel_db: Hotel.
    :return: hotel_photos: список ссылок на фотографии отеля.
    :rtype: List[str].
    """

    hotel_photos = []
    for i_image in hotel_db.images:
        hotel_photos.append(i_image.image)

    logger.debug('Отобраны фотографии для вывода пагинации.')
    return hotel_photos


@logger.catch
def table_hotel_output(hotel_id: int) -> Hotel:
    """
    Функция, получает нужный отель по его id и передает его в обработчик кнопок пагинации,
    для вывода фото отеля из таблицы images

    :param hotel_id: id отеля в БД.
    :type hotel_id: int.
    :return: запись в таблице hotels.
    :rtype: Hotel.
    """

    with db:
        # получаем отель по его id из БД
        hotel_db = Hotel.get(Hotel.id == hotel_id)

    logger.debug('Определен отель для вывода пагинации.')
    return hotel_db
