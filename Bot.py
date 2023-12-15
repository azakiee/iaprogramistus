import logging

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton
from telegram.ext import Updater, CallbackContext, Filters, Dispatcher, MessageHandler, CommandHandler
from telegram.ext import CallbackQueryHandler
from key import TOKEN
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import datetime
import requests
from FSM import register_handler, register

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def main():
    updater = Updater(token=TOKEN)
    dispatcher: Dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', do_start)
    keyboard_handler = CommandHandler('keyboard', do_keyboard)
    inline_keyboard_handler = CommandHandler('keyboard_inline', do_inline_keyboard)
    weather_handler = MessageHandler(Filters.text("weather"), do_weather)
    do_one_handler = MessageHandler(Filters.text("Раз"), do_one)
    do_two_handler = MessageHandler(Filters.text("Два"), do_two)
    get_cat_handler = CommandHandler("get_cat", get_cat)
    get_dog_handler = CommandHandler("get_dog", get_dog)
    set_timer_handler = CommandHandler('set', set_timer)
    stop_timer_handler = CommandHandler('stop', stop_timer)
    callback_handler = CallbackQueryHandler(keyboard_react)
    echo_handler = MessageHandler(Filters.text, do_echo)
    unknown_handler = MessageHandler(Filters.command, unknown)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(register_handler)
    dispatcher.add_handler(keyboard_handler)
    dispatcher.add_handler(get_cat_handler)
    dispatcher.add_handler(get_dog_handler)
    dispatcher.add_handler(inline_keyboard_handler)
    dispatcher.add_handler(stop_timer_handler)
    dispatcher.add_handler(set_timer_handler)
    dispatcher.add_handler(do_one_handler)
    dispatcher.add_handler(do_two_handler)
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
            f"<i>/set</i>",
            f"<i>/stop</i>",
            f"<i>/get_cat</i>",
            f"<i>/register</i>",
            f"<i>/get_dog</i>",
            f'<code>{name}</code> а остальное в разработке :3',
            "P.S: <i>что бы скопировать свой</i> <b>id</b>, <b>имя</b><i>, нажми на них.</i>"
            )

    text = '\n'.join(text)
    update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())


ERROR_MESSAGE = 'Ошибка при запросе к основному API: {error}'
URL = 'https://api.thecatapi.com/v1/images/search'
DOGS_URL = 'https://api.thedogapi.com/v1/images/search'
RESPONSE_USERNAME = 'Картинку {image_name} запросил: {username}, {name}'


def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(ERROR_MESSAGE.format(error=error))
        new_url = DOGS_URL
        response = requests.get(new_url)

    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


def get_cat(update, context):
    chat = update.effective_chat
    logging.info(RESPONSE_USERNAME.format(
        image_name='коти',
        username=chat.username,
        name=chat.first_name
    ))
    context.bot.send_photo(chat.id, get_new_image(), reply_markup=ReplyKeyboardRemove())


def get_new_image2():
    try:
        response = requests.get(DOGS_URL)
    except Exception as error:
        logging.error(ERROR_MESSAGE.format(error=error))
        new_url = URL
        response = requests.get(new_url)

    response = response.json()
    random_dog = response[0].get('url')
    return random_dog


def get_dog(update, context):
    chat = update.effective_chat
    logging.info(RESPONSE_USERNAME.format(
        image_name='пес',
        username=chat.username,
        name=chat.first_name
    ))
    context.bot.send_photo(chat.id, get_new_image2(), reply_markup=ReplyKeyboardRemove())


def do_keyboard(update: Update, context: CallbackContext):
    buttons = [
        ['/set', 'weather'],
        ['/get_cat', '/get_dog'],
        ['/stop', '/register'],
        ['Раз', 'Два'],
    ]
    user_id = update.message.from_user.id
    logger.info(f"{user_id=} Bызвaл функцию keyboard")
    text = "Жмякните на кнопочку ><"
    keyboard = ReplyKeyboardMarkup(buttons)
    update.message.reply_text(text, reply_markup=keyboard)


def do_inline_keyboard(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    logger.info(f'{user_id=} вызвал функцию do_inline_keyboard')
    buttons = [
        ['set', 'weather'],
        ['get_cat', 'get_dog'],
        ['stop', 'register'],
        ['Раз', 'Два']
    ]
    keyboard_buttons = [[InlineKeyboardButton(text=text, callback_data=text) for text in row] for row in buttons]
    keyboard = InlineKeyboardMarkup(keyboard_buttons)
    logger.info(f'Создана клавиатура {keyboard}')
    text = 'Выбери одну из опций на клавиатуре'
    update.message.reply_text(
        text,
        reply_markup=keyboard
    )
    logger.info(f'Ответ у пользователя')


def keyboard_react(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    logger.info(f'{user_id=} вызвал функцию keyboard_react')
    if query.data == 'get_cat':
        get_cat(update, context)
    if query.data == 'get_dog':
        get_dog(update, context)
    if query.data == 'weather':
        do_weather(update, context)
    if query.data == 'set':
        set_timer(update, context)
    if query.data == 'stop':
        stop_timer(update, context)
    if query.data == 'Раз':
        do_one(update, context)
    if query.data == 'Два':
        do_two(update, context)
    if query.data == 'register':
        register(update, context)


def do_weather(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    logger.info(f'{user_id=} Bызвaл функцию Weather')
    text = "Сейчас в Москве солнечно, но лучше просто посмотри в окно :)"

    context.bot.send_message(update.effective_chat.id, text, reply_markup=ReplyKeyboardRemove())


def do_one(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    name = update.effective_user.name
    logger.info(f'{user_id=} Bызвaл функцию do_one')
    text = f"Два-_- \n {name} Можно и нормальные кнопки нажать..."

    context.bot.send_message(update.effective_chat.id, text, reply_markup=ReplyKeyboardRemove())


def do_two(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    name = update.effective_user.name
    logger.info(f'{user_id=} Bызвaл функцию do_two')
    text = f"Три :/ \n {name} Можно и нормальные кнопки нажать..."

    context.bot.send_message(update.effective_chat.id, text, reply_markup=ReplyKeyboardRemove())


def set_timer(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    context.bot_data['user_id'] = user_id
    context.bot_data['timer'] = datetime.datetime.now()
    context.bot_data['timer_job'] = context.job_queue.run_repeating(show_seconds, 1)


def show_seconds(context: CallbackContext):
    logger.info(f'{context.job_queue.jobs()}')
    message_id = context.bot_data.get('message_id', None)
    user_id = context.bot_data['user_id']
    timer = datetime.datetime.now() - context.bot_data['timer']
    timer = timer.seconds
    text = f'прошло {timer} секунд'
    text += '\nнажмите /stop чтобы остановить таймер'
    if not message_id:
        message = context.bot.send_message(user_id, text)
        context.bot_data['message_id'] = message.message_id
    else:
        context.bot.edit_message_text(text, chat_id=user_id, message_id=message_id)


def stop_timer(update: Update, context: CallbackContext):
    logger.info(f'Запущена функция delete_timer')
    timer = datetime.datetime.now() - context.bot_data['timer']
    context.bot_data['timer_job'].schedule_removal()
    context.bot.send_message(update.effective_chat.id, f'Таймер остановлен. Прошло {timer} секунд')


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Друже, я такого не знаю")


if __name__ == "__main__":
    main()
