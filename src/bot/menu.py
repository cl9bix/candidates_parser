import logging
import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.bot import cfg
from src.bot.data_managment import get_all_categories, SendMessageFunc
from src.parsers import parser_workua

logger = logging.getLogger(__name__)


# def show_filters(update, context):
#     filters = filters_instance.filters
#     message = "\n".join([f"{key}: {value if value else 'не встановлено'}" for key, value in filters.items()])
#     update.message.reply_text(f"Ваші поточні фільтри:\n{message}")

def choose_search_method(update, context):
    SendMessageFunc(update, context, text='Оберіть метод пошуку', kb=InlineKeyboardMarkup(cfg.how_parse_kb))


def choose_category_workua(update, context):
    query = update.callback_query
    query.answer()
    page = int(query.data.split('_')[1]) if query.data.startswith('page_') else 0
    kb = get_all_categories(page=page, per_page=5, context=context)
    kb.append([InlineKeyboardButton('Вихід', callback_data='exit')])
    query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(kb))


def handle_category_selection(update, context):
    query = update.callback_query

    category_key = query.data
    category_map = context.user_data.get("category_map", {})
    category = category_map.get(category_key, None)

    if category:
        name = category["name"]
        url = category["url"]
        filters_instance.show_filters_menu(update, context)


def handle_filters_selection(update, context):
    query = update.callback_query
    filters_instance.show_filters_menu(update, context)


class Filters:
    def __init__(self):
        self.filters = {
            "position": None,
            "experience": None,
            "location": None,
            "salary_from": None,
            "salary_to": None,
            "preoccupancy": None,

        }

    def generate_filters_menu(self):
        filters_menu_kb = []

        if self.filters["position"]:
            filters_menu_kb.append(
                [InlineKeyboardButton(f"Посада: {self.filters['position']}", callback_data='enter_position')]
            )
        else:
            filters_menu_kb.append(
                [InlineKeyboardButton("Ввести посаду", callback_data='enter_position')]
            )

        if self.filters["experience"]:
            filters_menu_kb.append(
                [InlineKeyboardButton(f"Досвід: {self.filters['experience']}", callback_data='enter_experience')]
            )
        else:
            filters_menu_kb.append(
                [InlineKeyboardButton("Досвід роботи", callback_data='enter_experience')]
            )

        if self.filters["location"]:
            filters_menu_kb.append(
                [InlineKeyboardButton(f"Локація: {self.filters['location']}", callback_data='enter_location')]
            )
        else:
            filters_menu_kb.append(
                [InlineKeyboardButton("Обрати локацію", callback_data='enter_location')]
            )

        if self.filters["salary_from"]:
            filters_menu_kb.append(
                [InlineKeyboardButton(f"ЗП ВІД: {cfg.salaryfrom_dct[self.filters['salary_from']]}",
                                      callback_data='enter_salary_from')]
            )
        else:
            filters_menu_kb.append(
                [InlineKeyboardButton("Очікувана зп ВІД", callback_data='enter_salary_from')]
            )

        if self.filters["salary_to"]:
            filters_menu_kb.append(
                [InlineKeyboardButton(f"ЗП ДО: {cfg.salaryto_dct[self.filters['salary_to']]}",
                                      callback_data='enter_salary_to')]
            )
        else:
            filters_menu_kb.append(
                [InlineKeyboardButton("Очікувана зп ДО", callback_data='enter_salary_to')]
            )

        if self.filters["preoccupancy"]:
            filters_menu_kb.append(
                [InlineKeyboardButton(f"Зайнятість: {self.filters['preoccupancy']}",
                                      callback_data='enter_preoccupancy')]
            )
        else:
            filters_menu_kb.append(
                [InlineKeyboardButton("Вид зайнятості", callback_data='enter_preoccupancy')]
            )

        filters_menu_kb.append(
            [InlineKeyboardButton("ПОШУК ✅", callback_data='search')]
        )

        return InlineKeyboardMarkup(filters_menu_kb)

    def show_filters_menu(self, update, context):
        # self.filters['category_url'] = url
        query = update.callback_query
        query.answer()
        query.edit_message_text(
            text="Оберіть фільтр:",
            reply_markup=self.generate_filters_menu()
        )

    def reply_filters_menu(self, update, context):
        query = update.callback_query
        try:
            query.message.reply_text(
                text="Оберіть фільтр:",
                reply_markup=self.generate_filters_menu()
            )
        except Exception as e:
            update.message.reply_text(
                text="Оберіть фільтр:",
                reply_markup=self.generate_filters_menu()
            )

    def enter_position(self, update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(
            text="Введіть посаду(Розробник,дизайнер): ",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Назад", callback_data="filters_menu")]]
            )
        )
        context.user_data['action'] = 'get_position'

    def save_position(self, update, context):
        if update.callback_query:
            query = update.callback_query
        else:
            query = None

        position = update.message.text if update.message else None
        if not position:
            logger.error("Не вдалося отримати текст позиції.")
            return

        self.filters["position"] = position
        logger.info(f"USER {update.effective_user.username} WROTE POSITION: {position}")

        if query:
            query.message.reply_text(
                text="Оберіть фільтр:",
                reply_markup=self.generate_filters_menu()
            )
        else:
            update.message.reply_text(
                text="Оберіть фільтр:",
                reply_markup=self.generate_filters_menu()
            )

    def enter_experience(self, update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(
            text="Обеіть досвід роботи (у роках):",
            reply_markup=InlineKeyboardMarkup(
                cfg.exp_kb
            )
        )
        context.user_data['action'] = 'get_experience'

    def save_experience(self, update, context, exp_data):
        query = update.callback_query
        experience_key = int(exp_data)
        get_exp_for_user = cfg.exp_dct[experience_key]

        if get_exp_for_user is None:
            self.filters["experience"] = None

        self.filters["experience"] = get_exp_for_user
        logger.info(f"USER {update.effective_user.username} WROTE EXPERIENCE: {get_exp_for_user}")

        query.answer(
            text=f"Досвід роботи встановлено: {get_exp_for_user}",
        )
        SendMessageFunc(update, context, text='Оберіть фільтр',
                        kb=self.generate_filters_menu()
                        )

    def enter_location(self, update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(
            text="Введіть локацію:",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Назад", callback_data="filters_menu")]]
            )
        )
        context.user_data['action'] = 'get_location'

    def save_location(self, update, context):
        location: str = update.message.text
        self.filters["location"] = location.capitalize()
        # print(location.capitalize())
        logger.info(f"USER {update.effective_user.username} WROTE LOCATION: {location}")

        SendMessageFunc(update, context, text='Оберіть фільтр',
                        kb=self.generate_filters_menu()
                        )

    def enter_salary_from(self, update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(
            text="Оберіть зарплату ВІД",
            reply_markup=InlineKeyboardMarkup(cfg.salary_from_kb)
        )
        context.user_data['action'] = 'get_salary_from'

    def save_salary_from(self, update, context, salary_from):
        # print(salary_from,type(salary_from))
        get_salary_from_dct = cfg.salaryfrom_dct.get(str(salary_from))
        # print(get_salary_from_dct)
        self.filters["salary_from"] = salary_from
        SendMessageFunc(update, context, text='Оберіть фільтри', kb=self.generate_filters_menu())
        logger.info(f"USER {update.effective_user.username} WROTE SALARY_FROM: {salary_from}")

    def enter_salary_to(self, update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(
            text="Оберіть зарплату ДО",
            reply_markup=InlineKeyboardMarkup(cfg.salary_to_kb)
        )
        # context.user_data['action'] = 'get_salary_to'

    def save_salary_to(self, update, context, salary_to):
        get_salary_to_dct = cfg.salaryfrom_dct.get(str(salary_to))
        self.filters["salary_to"] = salary_to
        SendMessageFunc(update, context, text='Оберіть фільтри', kb=self.generate_filters_menu())
        logger.info(f"USER {update.effective_user.username} WROTE SALARY_TO: {salary_to}")

    def enter_preoccupancy(self, update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(
            text="Введіть тип зайнятості(Повна/Неповна):",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Назад", callback_data="filters_menu")]]
            )
        )
        context.user_data['action'] = 'get_preoccupancy'

    def save_preoccupancy(self, update, context):
        preoccupancy = update.message.text
        self.filters["preoccupancy"] = preoccupancy

        logger.info(f"USER {update.effective_user.username} WROTE PREOCCUPANCY: {preoccupancy}")

        SendMessageFunc(update, context, text='Оберіть фільтри', kb=self.generate_filters_menu())

    def search(self, update, context):
        data = self.filters
        send_candidates_url_to_user(update, context, data)

    def handler(self, update, context):
        action = context.user_data.get('action')

        if action == 'get_position':
            self.save_position(update, context)
        elif action == 'get_experience':
            self.save_experience(update, context)
        elif action == 'get_location':
            self.save_location(update, context)
        # elif action == 'get_salary_from':
        #     self.save_salary_from(update, context)
        # elif action == 'get_salary_to':
        #     self.save_salary_to(update, context)
        elif action == 'get_preoccupancy':
            self.save_preoccupancy(update, context)
        # elif action == 'run_search':
        #     parser_workua.parse_with_filters()

        context.user_data['action'] = None


def send_candidates_url_to_user(update, context, data: dict):
    query = update.callback_query
    response: list[dict] = parser_workua.parse_with_filters(filters=data)
    for idx, value in enumerate(response):
        query.message.reply_text(f'{idx + 1}.{value["name"]} - {value["url"]}')
    time.sleep(2)
    filters_instance.reply_filters_menu(update, context)


filters_instance = Filters()
