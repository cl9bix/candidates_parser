from telegram import InlineKeyboardButton

token = '7958850773:AAEafECUpxXfI5bP5h1xhXI0v8bwYyYGDCw'

how_parse_kb = [
    [InlineKeyboardButton('За категоріями(not working yet)', callback_data='by_category')],
    [InlineKeyboardButton('За фільтрацією', callback_data='by_filters')],
    [InlineKeyboardButton('Вихід', callback_data='exti')],

]

city_translations = {
    "Київ": "kyiv",
    "Одеса": "odesa",
    "Львів": "lviv",
    "Харків": "kharkiv",
    "Дніпро": "dnipro",
}

exp_dct = {
    1: 'До 1 року',
    164: 'Від 1 до 2 років',
    165: 'Від 2 до 5 років',
    166: 'Понад 5 років',
}

salaryfrom_dct = {
    '2': 10000,
    '3': 15000,
    '4': 20000,
    '5': 30000,
    '6': 40000,
    '7': 50000,
    '8': 100000,
}

salaryto_dct = {
    '2': 10000,
    '3': 15000,
    '4': 20000,
    '5': 30000,
    '6': 40000,
    '7': 50000,
    '8': 100000,
}

salary_from_kb = [
    [InlineKeyboardButton('10 000 грн', callback_data='salaryfrom_2')],
    [InlineKeyboardButton('15 000 грн', callback_data='salaryfrom_3')],
    [InlineKeyboardButton('20 000 грн', callback_data='salaryfrom_4')],
    [InlineKeyboardButton('30 000 грн', callback_data='salaryfrom_5')],
    [InlineKeyboardButton('40 000 грн', callback_data='salaryfrom_6')],
    [InlineKeyboardButton('50 000 грн', callback_data='salaryfrom_7')],
    [InlineKeyboardButton('100 000 грн', callback_data='salaryfrom_8')],
    [InlineKeyboardButton('Назад', callback_data='filters_menu')]
]
salary_to_kb = [
    [InlineKeyboardButton('10 000 грн', callback_data='salaryto_2')],
    [InlineKeyboardButton('15 000 грн', callback_data='salaryto_3')],
    [InlineKeyboardButton('20 000 грн', callback_data='salaryto_4')],
    [InlineKeyboardButton('30 000 грн', callback_data='salaryto_5')],
    [InlineKeyboardButton('40 000 грн', callback_data='salaryto_6')],
    [InlineKeyboardButton('50 000 грн', callback_data='salaryto_7')],
    [InlineKeyboardButton('100 000 грн', callback_data='salaryto_8')],
    [InlineKeyboardButton('Назад', callback_data='filters_menu')]
]

exp_kb = [
    # [InlineKeyboardButton('Без досвіду', callback_data='exp_0')],
    [InlineKeyboardButton('До 1 року', callback_data='exp_1')],
    [InlineKeyboardButton('Від 1 до 2 років', callback_data='exp_164')],
    [InlineKeyboardButton('Від 2 до 5 років', callback_data='exp_165')],
    [InlineKeyboardButton('Понад 5 років', callback_data='exp_166')],
    [InlineKeyboardButton('Назад', callback_data='filters_menu')],

]

filters_menu_kb = [
    [InlineKeyboardButton('Ввести посаду', callback_data='enter_position')],
    [InlineKeyboardButton('Досвід роботи', callback_data='enter_experience')],
    [InlineKeyboardButton('Обрати локацію', callback_data='enter_location')],
    [InlineKeyboardButton('Очікувана зп ВІД', callback_data='enter_salary_from')],
    [InlineKeyboardButton('Очікувана зп ДО', callback_data='enter_salary_to')],
    [InlineKeyboardButton('Вид зайнятості', callback_data='enter_preoccupancy')],
    [InlineKeyboardButton('ПОШУК ✅', callback_data='search')],
]

start_kb = [
    [InlineKeyboardButton('work.ua', callback_data='site_workua')],
    [InlineKeyboardButton('robota.ua(not working yet)', callback_data='site_robotaua')],
]

# search_candidate_kb = [
#     [InlineKeyboardButton('За категоріями', callback_data='searchby_category')],
#     [InlineKeyboardButton('За містами', callback_data='searchby_city')],
# ]
