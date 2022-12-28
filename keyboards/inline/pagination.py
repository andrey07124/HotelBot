from telegram_bot_pagination import InlineKeyboardPaginator
from loader import bot
from database.db_methods import table_images_output


def send_photo_page(message, hotel_db, page=1):
    photo_pages = table_images_output(hotel_db)

    paginator = InlineKeyboardPaginator(
        len(photo_pages),
        current_page=page,
        data_pattern='photo#{page}'
    )

    bot.send_message(
        message.chat.id,
        photo_pages[page-1],
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )
