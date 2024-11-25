from telegram import InlineKeyboardButton

token = '7958850773:AAEafECUpxXfI5bP5h1xhXI0v8bwYyYGDCw'


filters_menu_kb =[
    [InlineKeyboardButton('Ввести посаду',callback_data='enter_position')],
    [InlineKeyboardButton('Досвід роботи',callback_data='enter_experience')],
    [InlineKeyboardButton('Обрати локацію',callback_data='enter_location')],
    [InlineKeyboardButton('Очікувана зп ВІД',callback_data='enter_salary_from')],
    [InlineKeyboardButton('Очікувана зп ДО',callback_data='enter_salary_to')],
    [InlineKeyboardButton('Вид зайнятості',callback_data='enter_preoccupancy')],
    [InlineKeyboardButton('ПОШУК ✅',callback_data='search')],
]


start_kb = [
    [InlineKeyboardButton('work.ua', callback_data='site_workua')],
    [InlineKeyboardButton('robota.ua', callback_data='site_robotaua')],
]

search_candidate_kb = [
    [InlineKeyboardButton('За категоріями', callback_data='searchby_category')],
    [InlineKeyboardButton('За містами', callback_data='searchby_city')],
]

menu_kb = [
    [InlineKeyboardButton('123', callback_data='123')],
    [InlineKeyboardButton('123', callback_data='123')],
    [InlineKeyboardButton('123', callback_data='123')],
    [InlineKeyboardButton('123', callback_data='123')],
    [InlineKeyboardButton('123', callback_data='123')],
]
