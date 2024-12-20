import logging

from telegram import InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, Updater
from telegram.ext import MessageHandler, Filters as TgFilters

from src.bot import buttons, cfg
from src.bot.menu import filters_instance

logger = logging.getLogger(__name__)


def start(update, context):
    reply_markup = InlineKeyboardMarkup(cfg.start_kb)
    update.message.reply_text("Оберіть сайт для парсингу:", reply_markup=reply_markup)


if __name__ == '__main__':
    updater = Updater(cfg.token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(buttons.buttons))

    dp.add_handler(MessageHandler(TgFilters.text & ~TgFilters.command, filters_instance.handler))
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    logger.info("Бот стартанув")
    updater.start_polling()
    updater.idle()
