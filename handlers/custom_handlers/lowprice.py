from loader import bot
from states.states_information import UserInfoState  # Импортирую состояния
from telebot.types import Message
from keyboards.inline.city_markup import city  # Импортирую кнопки


@bot.message_handler(commands=['lowprice'])
def lowprice(message: Message) -> None:
    """Функция-хэндлер. Сначала присваивает пользователю состояние, после того как он ввел эту команду"""

    bot.set_state(message.from_user.id, UserInfoState.city_id, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['searching_state'] = 'PRICE_LOW_TO_HIGH'
    bot.send_message(message.from_user.id, f'Здравствуйте, {message.from_user.full_name}.'
                                           f' Укажите город для поиска отелей.')
    bot.register_next_step_handler(message, city)
