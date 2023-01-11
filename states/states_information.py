from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    """
    Класс, определяет состояния прохождения пользователя по этапам опроса.
    И для последующего хранения в них собранной от информации.

    Attributes:
        city_id (int): стейт для хранения id города из запроса.
        arrival_date (datetime): дата заселения в отель.
        departure_date (datetime): дата выезда из отеля.
        hotels_quantity (int): Количество отелей, которые необходимо вывести в результате
         (не больше заранее определённого максимума).
        is_photos (str): необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”).
        photo_quantity (int): при положительном ответе пользователь также вводит количество необходимых фотографий
         (не больше заранее определённого максимума).
        searching_state (str): сортировка в парсинге, в соответствии с введенной командой lowprice/hiprice/bestdeal.
        price_min (int): минимальная стоимость проживания в отеле.
        price_max (int): максимальная стоимость проживания в отеле.
        distance (int): удаление от центра города.
    """

    city_id = State()
    arrival_date = State()
    departure_date = State()
    hotels_quantity = State()
    is_photos = State()
    photo_quantity = State()
    searching_state = State()
    price_min = State()
    price_max = State()
    distance = State()
