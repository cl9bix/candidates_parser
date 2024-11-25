import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.bot.data_managment import get_all_categories
from src.parsers import parser_workua

logger = logging.getLogger(__name__)


def show_filters(update, context):
    filters = filters_instance.filters
    message = "\n".join([f"{key}: {value if value else 'не встановлено'}" for key, value in filters.items()])
    update.message.reply_text(f"Ваші поточні фільтри:\n{message}")


def choose_category_workua(update, context):
    query = update.callback_query
    query.answer()
    page = int(query.data.split('_')[1]) if query.data.startswith('page_') else 0
    kb = get_all_categories(page=page, per_page=5, context=context)
    query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(kb))


def handle_category_selection(update, context):
    query = update.callback_query

    category_key = query.data
    category_map = context.user_data.get("category_map", {})
    category = category_map.get(category_key, None)

    if category:
        name = category["name"]
        url = category["url"]
        filters_instance.show_filters_menu(update, context, url=url)


class Filters:
    def __init__(self):
        self.filters = {
            "position": None,
            "experience": None,
            "location": None,
            "salary_from": None,
            "salary_to": None,
            "preoccupancy": None,
            # "category_url": None,

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
                [InlineKeyboardButton(f"ЗП ВІД: {self.filters['salary_from']}", callback_data='enter_salary_from')]
            )
        else:
            filters_menu_kb.append(
                [InlineKeyboardButton("Очікувана зп ВІД", callback_data='enter_salary_from')]
            )

        if self.filters["salary_to"]:
            filters_menu_kb.append(
                [InlineKeyboardButton(f"ЗП ДО: {self.filters['salary_to']}", callback_data='enter_salary_to')]
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

    def show_filters_menu(self, update, context, url):
        # self.filters['category_url'] = url
        query = update.callback_query
        query.answer()
        query.edit_message_text(
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
        position = update.message.text
        self.filters["position"] = position

        logger.info(f"USER {update.effective_user.username} WROTE POSITION: {position}")

        update.message.reply_text(
            text=f"Позиція встановлена: {position}",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Повернутися до меню", callback_data="filters_menu")]]
            )
        )

    def enter_experience(self, update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(
            text="Введіть досвід роботи (у роках):",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Назад", callback_data="filters_menu")]]
            )
        )
        context.user_data['action'] = 'get_experience'

    def save_experience(self, update, context):
        experience = update.message.text
        self.filters["experience"] = experience

        logger.info(f"USER {update.effective_user.username} WROTE EXPERIENCE: {experience}")

        update.message.reply_text(
            text=f"Досвід роботи встановлено: {experience}",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Повернутися до меню", callback_data="filters_menu")]]
            )
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
        location = update.message.text
        self.filters["location"] = location

        logger.info(f"USER {update.effective_user.username} WROTE LOCATION: {location}")

        update.message.reply_text(
            text=f"Локація встановлена: {location}",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Повернутися до меню", callback_data="filters_menu")]]
            )
        )

    def enter_salary_from(self, update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(
            text="Введіть мінімальну зарплату:",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Назад", callback_data="filters_menu")]]
            )
        )
        context.user_data['action'] = 'get_salary_from'

    def save_salary_from(self, update, context):
        salary_from = update.message.text
        self.filters["salary_from"] = salary_from

        logger.info(f"USER {update.effective_user.username} WROTE SALARY_FROM: {salary_from}")

        update.message.reply_text(
            text=f"Мінімальна зарплата встановлена: {salary_from}",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Повернутися до меню", callback_data="filters_menu")]]
            )
        )

    def enter_salary_to(self, update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(
            text="Введіть максимальну зарплату:",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Назад", callback_data="filters_menu")]]
            )
        )
        context.user_data['action'] = 'get_salary_to'

    def save_salary_to(self, update, context):
        salary_to = update.message.text
        self.filters["salary_to"] = salary_to

        logger.info(f"USER {update.effective_user.username} WROTE SALARY_TO: {salary_to}")

        update.message.reply_text(
            text=f"Максимальна зарплата встановлена: {salary_to}",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Повернутися до меню", callback_data="filters_menu")]]
            )
        )

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

        update.message.reply_text(
            text=f"Тип зайнятості встановлено: {preoccupancy}",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Повернутися до меню", callback_data="filters_menu")]]
            )
        )

    def search(self, update, context):
        data = self.filters
        # context.user_data['action'] = 'run_search'
        parser_workua.parse_with_filters(data)

    def handler(self, update, context):
        action = context.user_data.get('action')

        if action == 'get_position':
            self.save_position(update, context)
        elif action == 'get_experience':
            self.save_experience(update, context)
        elif action == 'get_location':
            self.save_location(update, context)
        elif action == 'get_salary_from':
            self.save_salary_from(update, context)
        elif action == 'get_salary_to':
            self.save_salary_to(update, context)
        elif action == 'get_preoccupancy':
            self.save_preoccupancy(update, context)
        # elif action == 'run_search':
        #     parser_workua.parse_with_filters()

        context.user_data['action'] = None


filters_instance = Filters()
