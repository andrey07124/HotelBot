from loader import bot
from states.states_information import UserInfoState  # Импортирую состояния
from telebot.types import Message
from keyboards.inline.city_markup import city  # Импортирую кнопки
from utils.request_to_api_post import hotels_founding_bestdeal, photo_founding
from database.db_methods import table_users_filling, table_hotels_filling, table_images_filling
from keyboards.inline.pagination import send_photo_page


@bot.message_handler(commands=['bestdeal'])
def bestdeal(message: Message) -> None:
    """
    Функция-хэндлер. Сначала присваивает пользователю состояние city_id, после того как он ввел команду bestdeal.
    Просит указать город для поиска отелей.

    :param message: объект Message, с отправленным пользователем сообщением.
    """

    bot.set_state(message.from_user.id, UserInfoState.city_id, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['searching_state'] = 'DISTANCE'
    bot.send_message(message.from_user.id, f'Здравствуйте, {message.from_user.full_name}.'
                                           f' Укажите город для поиска отелей.')
    bot.register_next_step_handler(message, city)


@bot.message_handler(state=UserInfoState.price_min)
def get_hotels_quantity(message: Message) -> None:
    """
    Функция-хендлер. Ловит состояние price_min, записывает минимальную цену из сообщения пользователя в стейт.
    Просит ввести максимальную цену.

    :param message: объект Message, с отправленным пользователем сообщением.
    """

    price_min = message.text
    if price_min.isdigit() and int(price_min) >= 0:
        bot.set_state(message.from_user.id, UserInfoState.price_max, message.chat.id)
        bot.send_message(message.from_user.id, 'Введите максимальную цену в USD.')

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['price_min'] = int(price_min)

    else:  # Если введено не число, повторяю запрос
        bot.send_message(message.from_user.id,
                         'Введите цену числом.')


@bot.message_handler(state=UserInfoState.price_max)
def get_hotels_quantity(message: Message) -> None:
    """
    Функция-хендлер. Ловит состояние price_max, записывает максимальную цену из сообщения пользователя в стейт.
    Просит ввести максимальное удаление от центра.

    :param message: объект Message, с отправленным пользователем сообщением.
    """

    price_max = message.text
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:

        if price_max.isdigit() and int(price_max) >= data['price_min']:
            bot.set_state(message.from_user.id, UserInfoState.distance, message.chat.id)
            bot.send_message(message.from_user.id, 'Введите максимальное удаление отеля от центра в километрах.')
            data['price_max'] = int(price_max)

        else:  # Если введено не число, повторяю запрос
            bot.send_message(message.from_user.id,
                             'Введите цену числом, большим минимальной цены.')


@bot.message_handler(state=UserInfoState.distance)
def get_hotels_quantity(message: Message) -> None:
    """
    Функция-хендлер. Ловит состояние distance, записывает максимальное удаление от центра
    из сообщения пользователя в стейт. Осуществляет вывод информации по отелям, в том числе фото с пагинацией.

    :param message: объект Message, с отправленным пользователем сообщением.
    """

    distance = message.text
    if distance.isdigit() and int(distance) >= 0:
        bot.send_message(message.from_user.id, 'Подождите, идет поиск отелей...')

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['distance'] = int(distance)

        hotels = hotels_founding_bestdeal(data)
        if isinstance(hotels, list):
            # Заполнение пользователей в БД:
            # Вывод полного имени через call
            user = table_users_filling(message.from_user.full_name,
                                       message.chat.id, data['searching_state'])  # таблица № 1
            for i_hotel in hotels:
                bot.send_message(message.from_user.id,
                                 f'Название отеля: {i_hotel["name"]}\n'
                                 f'Стоимость: {i_hotel["price"]} USD\n'
                                 f'Расстояние до центра: {i_hotel["distance_from_destination"]}\n'
                                 f'Адрес: {i_hotel["address_line"]}')

                # Заполнение отелей в БД:
                hotel_db = table_hotels_filling(user, i_hotel["name"], i_hotel["address_line"])  # таблица № 2

                if data['is_photos'] == 'yes':
                    for i_photo in photo_founding(i_hotel['hotel_id'], data):
                        # bot.send_message(message.from_user.id, f'{i_photo}')  # вывод фото без пагинации

                        # Заполнение фото в БД:
                        table_images_filling(hotel_db, i_photo)  # таблица № 3

                    send_photo_page(message, hotel_db)  # пагинация фото, начало

            bot.delete_state(message.from_user.id, message.chat.id)  # Отмена стейтов,
            # чтобы они не мешали следующим командам

        elif isinstance(hotels, str):
            bot.send_message(message.from_user.id, hotels)  # выводит что не найдено
            bot.delete_state(message.from_user.id, message.chat.id)  # Отмена стейтов,
            # чтобы они не мешали следующим командам

        bot.set_state(message.from_user.id, None, message.chat.id)

    else:  # Если введено не число, повторяю запрос
        bot.send_message(message.from_user.id,
                         'Введите расстояние числом.')
