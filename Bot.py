import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CallbackContext, Filters, Dispatcher, MessageHandler, CommandHandler
from set import TOKEN


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def main():
    updater = Updater(token = TOKEN)
    dispatcher: Dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', do_start)
    echo_handler = MessageHandler(Filters.text, do_echo)
    keyboard_handler = CommandHandler('keyboard', do_keyboard)
    weather_handler = CommandHandler("Weather", do_weather)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(keyboard_handler)
    dispatcher.add_handler(weather_handler)
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
    update.message.reply_text(answer)


def do_start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    logger.info(f'{user_id=} Bызвaл функцию start')
    text = ("Приветствую тебя, кожаный мешок!\n"
            f"Tвoй {user_id=}\nЯ знаю команды /start и /keyboard")


    update.message.reply_text(text)


def do_keyboard(update: Update, context: CallbackContext):
    buttons = [
        ["Раз", "Два"],
        ["Три", "Четыре"],
        ["Weather"]
    ]
    user_id = update.message.from_user.id
    logger.info(f"{user_id=} Bызвaл функцию keyboard")
    text = "Жмякните на кнопочку ><"
    keyboard = ReplyKeyboardMarkup(buttons)
    update.message.reply_text(text, reply_markup=keyboard)


def do_weather(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    logger.info(f'{user_id=} Bызвaл функцию Weather')
    text = "Сейчас в Москве солнечно, но возможно я вру :)"

    update.message.reply_text(text)



if __name__ == "__main__":
    main()