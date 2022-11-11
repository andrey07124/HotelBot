from telebot.types import Message
from loader import bot


@bot.message_handler(content_types=['text'])
def bot_greeting(message: Message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, f'Привет <b>{message.from_user.full_name}</b>!', parse_mode='html')
