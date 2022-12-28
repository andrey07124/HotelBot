from database.database_init import db, User, Hotel, Image
from peewee import *
from loguru import logger


@logger.catch
def table_users_filling(name, telegram_id, command):
    """Заполнение таблицы users"""

    command_selection = {'PRICE_LOW_TO_HIGH': '/lowprice',
                         'PRICE_HIGH_TO_LOW': '/highprice',
                         'DISTANCE': '/bestdeal'}
    with db:
        user = User.create(name=name, telegram_id=telegram_id, command=command_selection[command])
    logger.debug('Внесена запись в таблицу users')
    return user


@logger.catch
def table_hotels_filling(user, hotel, address):
    """Заполнение таблицы hotels"""

    with db:
        hotel_bd = Hotel.create(user=user, hotel=hotel, address=address)
        logger.debug('Внесена запись в таблицу hotels')
    return hotel_bd


@logger.catch
def table_images_filling(hotel, image):
    """Заполнение таблицы images"""

    with db:
        Image.create(hotel=hotel, image=image)
        logger.debug('Внесена запись в таблицу images')


@logger.catch
def table_users_output(telegram_id):
    """Функция, передающая для вывода историю таблицы users"""

    with db:
        # отбираем для вывода 5 последних записей истории из БД
        query = User.select().where(User.telegram_id == telegram_id).limit(5).order_by(User.id.desc())
        logger.debug('Отобраны запросы для вывода истории.')
    return query


@logger.catch
def table_images_output(hotel_db):
    """Функция, передающая для вывода историю таблицы images"""

    hotel_photos = []
    for i_image in hotel_db.images:
        hotel_photos.append(i_image.image)
    # with db:
    #     # отбираем фото по id отеля из БД
    #     query = Image.select().where(Image.hotel.id == hotel_id)

    logger.debug('Отобраны фотографии для вывода пагинации.')
    logger.debug(hotel_photos)
    return hotel_photos
