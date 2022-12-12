from loader import bot
from states.states_information import UserInfoState
from telebot.types import Message, CallbackQuery
from keyboards.inline.city_markup import city
from keyboards.inline.is_photos_markup import is_photo_markup
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
import datetime
from utils.request_to_api_post import hotels_founding, photo_founding


@bot.callback_query_handler(func=None, state=UserInfoState.city_id)
def city_callback(call: CallbackQuery) -> None:
    """ Функция, ловит callback нажатой пользователем кнопки, просит ввести дату заезда
    и устанавливает состояние arrival_date """
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['city_id'] = call.data  # сохраняем полученные данные в словарь

    # Создаю календарь для даты заселения
    calendar, step = DetailedTelegramCalendar(calendar_id=1, min_date=datetime.date.today()).build()
    bot.send_message(call.from_user.id,
                     f'Введите планируемую дату заселения в отель: {LSTEP[step]}',
                     reply_markup=calendar)
    bot.set_state(call.from_user.id, UserInfoState.arrival_date, call.message.chat.id)


@bot.message_handler(state=UserInfoState.city_id)
def repeat_get_city(message: Message) -> None:
    """Функция, осуществляет повторный вызов клавиатуры выбора города при неверном вводе"""
    bot.send_message(message.from_user.id, 'Выберите один из предложенных вариантов:',
                     reply_markup=city(message))


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def get_arrival_date(call: CallbackQuery) -> None:
    """ Функция-хэндлер. Ловит callback выбранной в календаре даты прибытия и сохраняет ее.
    Просит ввести дату выезда из отеля """
    today_date = datetime.date.today()
    result, key, step = DetailedTelegramCalendar(calendar_id=1, min_date=today_date, locale='ru').process(call.data)
    if not result and key:
        bot.edit_message_text(f'Дата заселения. Выберите {LSTEP[step]}',
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f'Вы выбрали дату заселения: {result}.',
                              call.message.chat.id,
                              call.message.message_id)

        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['arrival_date'] = result

        # Создаю календарь для даты выезда
        calendar, step = DetailedTelegramCalendar(calendar_id=2, min_date=result, locale='ru').build()
        bot.send_message(call.from_user.id,
                         f'Введите планируемую дату выезда из отеля: {LSTEP[step]}',
                         reply_markup=calendar)
        bot.set_state(call.from_user.id, UserInfoState.departure_date, call.message.chat.id)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def get_date_in(call: CallbackQuery) -> None:
    """ Функция-хэндлер. Ловит callback выбранной в календаре даты выезда из отеля и сохраняет ее.
    Просит ввести дату выезда из отеля """
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        arrival_date = data['arrival_date']
        # TODO как можно напрямую без контекстного менеджера получить значение из состояния
    result, key, step = DetailedTelegramCalendar(calendar_id=2, min_date=arrival_date, locale='ru').process(call.data)
    if not result and key:
        bot.edit_message_text(f'Дата выезда из отеля. Выберите {LSTEP[step]}',
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f'Вы выбрали дату выезда из отеля: {result}',
                              call.message.chat.id,
                              call.message.message_id)

        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['departure_date'] = result

        bot.send_message(call.from_user.id, 'Введите количество отелей которые необходимо вывести'
                                            ' (не более 25).')
        bot.set_state(call.from_user.id, UserInfoState.hotels_quantity, call.message.chat.id)


@bot.message_handler(state=UserInfoState.hotels_quantity)
def get_hotels_quantity(message: Message) -> None:
    """Функция-хендлер. Ловит состояние hotels_quantity, записывает его значение из сообщения пользователя"""
    hotels_quantity = message.text
    if hotels_quantity.isdigit() and 0 < int(hotels_quantity) < 26:
        bot.send_message(message.from_user.id, 'Нужно ли показать фотографии', reply_markup=is_photo_markup())
        bot.set_state(message.from_user.id, UserInfoState.is_photos, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['hotels_quantity'] = int(hotels_quantity)
    else:  # Если введено не число от 1 до 25, повторяю запрос
        bot.send_message(message.from_user.id,
                         'Введите числом от 1 до 25 количество отелей которые необходимо вывести.')


@bot.callback_query_handler(func=None, state=UserInfoState.is_photos)
def get_is_photo(call: CallbackQuery) -> None:
    """Функция-хэндлер. Ловит callback нажатой пользователем кнопки, записывает нужны ли фото.
    Если нужны - просит ввести количество фотографий для вывода, и устанавливает состояние photo_quantity.
    Если не нужны - выводит результат."""
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['is_photos'] = call.data
    if call.data == 'yes':
        bot.send_message(call.from_user.id, 'Сколько фотографий показать?')
        bot.set_state(call.from_user.id, UserInfoState.photo_quantity, call.message.chat.id)
    elif call.data == 'no':
        hotels = hotels_founding(data)
        if data['searching_state'] == 'DISTANCE':  # для bestdeal
            bot.set_state(call.from_user.id, UserInfoState.price_min, call.message.chat.id)
            bot.send_message(call.from_user.id, 'Введите минимальную цену в USD.')
        else:
            if isinstance(hotels, list):
                for i_hotel in hotels:
                    bot.send_message(call.from_user.id,
                                     f'Название отеля: {i_hotel["name"]}\n'
                                     f'Стоимость: {i_hotel["price"]} USD\n'
                                     f'Расстояние до центра: {i_hotel["distance_from_destination"]}\n'
                                     f'Адрес: {i_hotel["address_line"]}')
            elif isinstance(hotels, str):  # Если отели не найдены
                bot.send_message(call.from_user.id, hotels)


@bot.message_handler(state=UserInfoState.is_photos)
def repeat_get_city(message: Message) -> None:
    """Функция, осуществляет повторный вызов клавиатуры по фотографиям при неверном вводе"""
    bot.send_message(message.from_user.id, 'Выберите один из предложенных вариантов:',
                     reply_markup=is_photo_markup())


@bot.message_handler(state=UserInfoState.photo_quantity)
def get_photo_quantity(message: Message) -> None:
    """
    Функция-хендлер. Ловит состояние photo_quantity, записывает количество фото из сообщения пользователя.
    Осуществляет вывод информации по отелям
    """
    photo_quantity = message.text
    if photo_quantity.isdigit() and 0 < int(photo_quantity) < 26:

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photo_quantity'] = int(photo_quantity)

        hotels = hotels_founding(data)
        if data['searching_state'] == 'DISTANCE':  # для bestdeal
            bot.set_state(message.from_user.id, UserInfoState.price_min, message.chat.id)
            bot.send_message(message.from_user.id, 'Введите минимальную цену в USD.')
        else:
            if isinstance(hotels, list):
                for i_hotel in hotels:
                    bot.send_message(message.from_user.id,
                                     f'Название отеля: {i_hotel["name"]}\n'
                                     f'Стоимость: {i_hotel["price"]} USD\n'
                                     f'Расстояние до центра: {i_hotel["distance_from_destination"]}\n'
                                     f'Адрес: {i_hotel["address_line"]}')

                    for i_photo in photo_founding(i_hotel['hotel_id'], data):  # вывод фото
                        bot.send_message(message.from_user.id, f'{i_photo}')
            elif isinstance(hotels, str):
                bot.send_message(message.from_user.id, hotels)  # выводит что отели не найдены

    else:  # Если введено не число от 1 до 25, повторяю запрос
        bot.send_message(message.from_user.id,
                         'Введите числом от 1 до 25 количество отелей которые необходимо вывести')
