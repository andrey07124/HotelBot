from loader import bot
from states.states_information import UserInfoState  # Импортирую состояния
from telebot.types import Message
from keyboards.inline.city_markup import city  # Импортирую кнопки
from utils.request_to_api_post import hotels_founding_bestdeal, photo_founding


@bot.message_handler(commands=['bestdeal'])
def bestdeal(message: Message) -> None:
    """Функция-хэндлер. Сначала присваивает пользователю состояние, после того как он ввел команду bestdeal"""

    bot.set_state(message.from_user.id, UserInfoState.city_id, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['searching_state'] = 'DISTANCE'
    bot.send_message(message.from_user.id, f'Здравствуйте, {message.from_user.full_name}.'
                                           f' Укажите город для поиска отелей.')
    bot.register_next_step_handler(message, city)


@bot.message_handler(state=UserInfoState.price_min)
def get_hotels_quantity(message: Message) -> None:
    """Функция-хендлер. Ловит состояние price_min, записывает его значение из сообщения пользователя"""
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
    """Функция-хендлер. Ловит состояние price_max, записывает его значение из сообщения пользователя"""
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
    Функция-хендлер. Ловит состояние distance, записывает его значение из сообщения пользователя.
    Осуществляет вывод информации по отелям
    """

    distance = message.text
    if distance.isdigit() and int(distance) >= 0:
        bot.send_message(message.from_user.id, 'Подождите, идет поиск отелей...')

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['distance'] = int(distance)

        hotels = hotels_founding_bestdeal(data)
        print(hotels)
        if isinstance(hotels, list):
            for i_hotel in hotels:
                bot.send_message(message.from_user.id,
                                 f'Название отеля: {i_hotel["name"]}\n'
                                 f'Стоимость: {i_hotel["price"]} USD\n'
                                 f'Расстояние до центра: {i_hotel["distance_from_destination"]}\n'
                                 f'Адрес: {i_hotel["address_line"]}')
                if data['is_photos'] == 'yes':
                    for i_photo in photo_founding(i_hotel['hotel_id'], data):  # вывод фото
                        bot.send_message(message.from_user.id, f'{i_photo}')
        elif isinstance(hotels, str):
            bot.send_message(message.from_user.id, hotels)  # выводит что не найдено

    else:  # Если введено не число, повторяю запрос
        bot.send_message(message.from_user.id,
                         'Введите расстояние числом.')
