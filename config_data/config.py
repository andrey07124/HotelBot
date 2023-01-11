import os
from dotenv import load_dotenv, find_dotenv  # подгружаем токены и пароли

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('echo', "Повтор сообщения"),
    ('hello_world', 'Отправляет Hello world!'),
    ('lowprice', 'Узнать топ самых дешёвых отелей'),
    ('highprice', 'Узнать топ самых дорогих отелей'),
    ('bestdeal', 'Узнать топ самых выгодных предложений'),
    ('history', 'Узнать историю поиска отелей')
)
