from src.bot import menu
from src.bot.menu import filters_instance


def buttons(update, context):
    query = update.callback_query
    if query.data == 'site_workua':
        menu.choose_search_method(update, context)
    elif query.data == 'by_filters':
        menu.handle_filters_selection(update, context)
    # elif query.data.startswith('category_'):
    #     category = query.data.split('_')[1]
    # elif query.data.startswith("page_"):
    #     menu.choose_category_workua(update, context)
    # elif query.data.startswith("cat_"):
    #     menu.handle_category_selection(update, context)
    elif query.data == 'filters_menu':
        filters_instance.show_filters_menu(update, context)
    elif query.data == 'enter_position':
        filters_instance.enter_position(update, context)
    # elif query.data == 'enter_position':
    #     filters_instance.enter_position(update, context)
    elif query.data == 'enter_experience':
        filters_instance.enter_experience(update, context)

    elif query.data.startswith('exp_'):
        exp_data = query.data.split('_')[1]
        filters_instance.save_experience(update, context, exp_data)
    elif query.data == 'enter_location':
        filters_instance.enter_location(update, context)
    elif query.data == 'enter_salary_from':
        filters_instance.enter_salary_from(update, context)
    elif query.data == 'enter_salary_to':
        filters_instance.enter_salary_to(update, context)
    elif query.data == 'enter_preoccupancy':
        filters_instance.enter_preoccupancy(update, context)
    elif query.data == 'search':
        filters_instance.search(update, context)

    elif query.data.startswith('salaryfrom_'):
        salary_from = query.data.split('_')[1]
        menu.filters_instance.save_salary_from(update, context, salary_from)

    elif query.data.startswith('salaryto_'):
        salary_to = query.data.split('_')[1]
        menu.filters_instance.save_salary_to(update, context, salary_to)
