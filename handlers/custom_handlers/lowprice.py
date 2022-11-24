from loader import bot
from states.lowprice_information import UserInfoState  # Импортирую состояния
from telebot.types import Message, CallbackQuery
from keyboards.reply.city_markup import city  # Импортирую кнопки


@bot.message_handler(commands=['lowprice'])
def lowprice(message: Message) -> None:
    """Функция-хэндлер. Сначала присваивает пользователю состояние, после того как он ввел эту команду"""
    bot.set_state(message.from_user.id, UserInfoState.city_id, message.chat.id)
    bot.send_message(message.from_user.id, f'Здравствуйте, {message.from_user.full_name}.'
                                           f' Укажите город для поиска отелей.')
    bot.register_next_step_handler(message, city)


@bot.callback_query_handler(func=None)  # TODO не понимаю какой поставить фильтр
def city_callback(call: CallbackQuery) -> None:
    """Функция, ловит callback нажатой пользователем кнопки"""
    if call.data:
        with bot.retrieve_data(call.message.from_user.id, call.message.chat.id) as data:
            data['city_id'] = call.data
        print(UserInfoState.city_id)
        bot.send_message(call.message.from_user.id, 'Введите планируемую дату заселения в отель.')
        bot.set_state(call.message.from_user.id, UserInfoState.date_in, call.message.chat.id)
    else:
        bot.send_message(call.message.from_user.id, 'Выберите один из предложенных вариантов:',
                         reply_markup=city(call.message))  # повторный вызов клавиатуры при неверном вводе


@bot.message_handler(state=UserInfoState.city_id)
def get_city(message: Message) -> None:
    """Функция-хэндлер. Ловит состояние которое ранее присвоено пользователю (city) и сохраняет его"""

    bot.send_message(message.from_user.id, 'Введите планируемую дату заселения в отель.')
    bot.set_state(message.from_user.id, UserInfoState.date_in, message.chat.id)


    # with bot.retrieve_data(message.from_user.id, message.chat.id) as data:  # сохраняем полученные данные в словарь
    #     data['city'] = message.text


@bot.message_handler(state=UserInfoState.date_in)
def get_date_in(message: Message) -> None:
    """Функция-хэндлер. Ловит состояние date_in и сохраняет его"""
    bot.send_message(message.from_user.id, 'Введите планируемую дату выезда из отеля.')
