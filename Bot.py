import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CallbackContext, Filters, Dispatcher, MessageHandler, CommandHandler
from telegram.ext import CallbackQueryHandler
from set import TOKEN
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def main():
    updater = Updater(token = TOKEN)
    dispatcher: Dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', do_start)
    keyboard_handler = CommandHandler('keyboard', do_keyboard)
    inline_keyboard_handler = CommandHandler('keyboard_inline', do_inline_keyboard)
    weather_handler = MessageHandler(Filters.text("weather"), do_weather)
    echo_handler = MessageHandler(Filters.text, do_echo)
    unknown_handler = MessageHandler(Filters.command, unknown)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(keyboard_handler)
    dispatcher.add_handler(inline_keyboard_handler)
    dispatcher.add_handler(weather_handler)
    dispatcher.add_handler(unknown_handler)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    logging.info(updater.bot.getMe())
    updater.idle()


def do_echo(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    name = update.message.from_user.name
    text = update.message.text

    logging.info(f"{name=} {user_id=} вызвал функцию echo")
    answer = f"Твой {user_id=}\nТвой {name=}\nТы написал {text=}"

    update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove())


def do_start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    logger.info(f'{user_id=} Bызвaл функцию start')
    text = ("Салямалейкум!\n"
            f"Я знаю твой {user_id=} :| \nЯ знаю команды /start и /keyboard и /keyboard_inline")

    update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())


def do_keyboard(update: Update, context: CallbackContext):
    buttons = [
        ["Раз", "Два"],
        ["Три", "Четыре"],
        ["weather"]
    ]
    user_id = update.message.from_user.id
    logger.info(f"{user_id=} Bызвaл функцию keyboard")
    text = "Жмякните на кнопочку ><"
    keyboard = ReplyKeyboardMarkup(buttons)
    update.message.reply_text(text, reply_markup=keyboard)


def do_inline_keyboard(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    logger.info(f"{user_id=} Bызвaл функцию do_inline_keyboard")
    buttons = [
        ["Раз", "Два"],
        ["Три", "Четыре"],
        ["weather"]
    ]
    keyboard_button = [[InlineKeyboardButton(text=text, callback_data=text) for text in row] for row in buttons]
    keyboard = InlineKeyboardMarkup(keyboard_button)
    logger.info(f"Создана клавиатура {keyboard}")
    text = "Выбери одну из кнопок на клавиатуре"
    update.message.reply_text(
        text,
        reply_markup=keyboard
    )


def do_weather(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    logger.info(f'{user_id=} Bызвaл функцию Weather')
    text = "Сейчас в Москве солнечно, но возможно я вру :)"

    update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text = "Друже, что это?")


if __name__ == "__main__":
    main()
