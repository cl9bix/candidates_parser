from telegram import InlineKeyboardButton

from src.parsers import parser_workua

CATEGORIES_PER_PAGE = 5


def get_paginated_categories(data, page):
    start = page * CATEGORIES_PER_PAGE
    end = start + CATEGORIES_PER_PAGE
    return data[start:end]


def get_all_categories(page, per_page, context):
    categories = parser_workua.fetch_categories()
    total_pages = (len(categories) + per_page - 1) // per_page

    context.user_data["category_map"] = {
        f"cat_{i}": {"name": cat["name"], "url": cat["url"]}
        for i, cat in enumerate(categories)
    }

    start = page * per_page
    end = start + per_page
    kb = [
        [InlineKeyboardButton(cat["name"], callback_data=f"cat_{i}")]
        for i, cat in enumerate(categories[start:end])
    ]

    navigation_buttons = []
    if start > 0:
        navigation_buttons.append(InlineKeyboardButton("⬅️ Попередня", callback_data=f"page_{page - 1}"))
    navigation_buttons.append(InlineKeyboardButton(f"{page + 1}/{total_pages}", callback_data="current_page"))
    if end < len(categories):
        navigation_buttons.append(InlineKeyboardButton("➡️ Наступна", callback_data=f"page_{page + 1}"))

    if navigation_buttons:
        kb.append(navigation_buttons)

    return kb


def SendMessageFunc(update, context, text: str, kb):
    query = update.callback_query
    if query:
        try:
            query.message.edit_text(
                text=text,
                reply_markup=kb
            )
        except Exception as e:
            query.message.reply_text(
                text=text,
                reply_markup=kb
            )

    else:
        try:
            update.message.edit_text(
                text=text,
                reply_markup=kb
            )
        except Exception as e:
            update.message.reply_text(
                text=text,
                reply_markup=kb
            )
