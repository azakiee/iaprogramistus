import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import Updater, CallbackContext, Filters, Dispatcher, MessageHandler, CommandHandler
from telegram.ext import CallbackQueryHandler
from key import TOKEN
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
    callback_handler = CallbackQueryHandler(keyboard_react)
    echo_handler = MessageHandler(Filters.text, do_echo)
    unknown_handler = MessageHandler(Filters.command, unknown)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(keyboard_handler)
    dispatcher.add_handler(inline_keyboard_handler)
    dispatcher.add_handler(weather_handler)
    dispatcher.add_handler(callback_handler)
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
    name = update.message.from_user.name
    logger.info(f'{user_id=} Bызвaл функцию start')
    text = ("Салямалейкум!",
            f"Я знаю твой id: <code><b>{user_id}</b></code> -_-",
            f"Я знаю команды: ",
            f"<i>/start</i>",
            f"<i>/keyboard</i>",
            f"<i>/keyboard_inline</i>",
            f'<code>{name}</code> а остальное в разработке :3',
            "P.S: <i>что бы скопировать свой</i> <b>id</b>, <b>имя</b><i>, нажми на них.</i>"
            )

    text = '\n'.join(text)
    update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())


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

def keyboard_react(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = update.effective_user.id
    logger.info(f'{user_id=} вызвал функцию keyboard_react')
    buttons = [
        ['Раз', 'Два'],
        ['Три', 'Четыре'],
        ['weather']
    ]
    for row in buttons:
        if query.data in row:
            row.pop(row.index(query.data))
    keyboard_buttons = [[InlineKeyboardButton(text=text, callback_data=text) for text in row] for row in buttons]
    keyboard = InlineKeyboardMarkup(keyboard_buttons)
    text = 'Выбери другую опцию на клавиатуре'
    query.edit_message_text(
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
                             text = "Друже, я такого не знаю?")


if __name__ == "__main__":
    main()