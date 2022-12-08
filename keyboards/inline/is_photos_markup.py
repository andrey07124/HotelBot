from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def is_photo_markup() -> InlineKeyboardMarkup:
    """Функция, создающая клавиатуру с кнопками запроса необходимости вывода фотографий"""
    photo_keyboard = InlineKeyboardMarkup()
    yes_button = InlineKeyboardButton(text='Да', callback_data='yes')
    no_button = InlineKeyboardButton(text='нет', callback_data='no')
    photo_keyboard.add(yes_button, no_button)

    return photo_keyboard
