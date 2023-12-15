import logging
from typing import List

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, InlineKeyboardButton
from telegram.ext import Updater, CallbackContext, Filters, Dispatcher, MessageHandler, CommandHandler
from telegram.ext import CallbackQueryHandler
from key import TOKEN
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import datetime
import requests
from telegram.ext import ConversationHandler
from db import write_to_db, find_user_by_id

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


WAIT_NAME, WAIT_SURNAME, WAIT_BIRTHDAY, WAIT_SEX, WAIT_GRADE, WAIT_OK = range(6)


def check_register(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    logger.info(f'{username=} {user_id=} вызвал функцию check_register')
    user = find_user_by_id(user_id)
    if not user:
        return ask_name(update, context)

    answer = [f'Привет!',
              f'Ты уже зарегистрирован со следующими данными:\n',
              f'Имя: {user[1]}',
              f'Фамилия: {user[2]}',
              f'Дата рождения: {user[3]}']
    answer = '\n'.join(answer)
    update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove())

    buttons = [InlineKeyboardButton(text='Да', callback_data='Да'),
               InlineKeyboardButton(text='Нет', callback_data='Нет')]
    keyboard = InlineKeyboardMarkup.from_row(buttons)
    update.message.reply_text(text='Вы хотите повторно зарегистрироваться?', reply_markup=keyboard)
    return WAIT_OK


def get_yes_no(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    logger.info(f'{username=} {user_id=} вызвал функцию get_yes_no')
    query = update.callback_query
    if query.data == 'Да':
        return ask_name(update, context)
    return ConversationHandler.END


def ask_name(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    logger.info(f'{username=} {user_id=} вызвал функцию ask_name')
    answer = [
        f'Привет!',
        f'Назови свое имя'
    ]
    answer = '\n'.join(answer)
    update.message.reply_text(answer, reply_markup=ReplyKeyboardRemove())

    return WAIT_NAME


def get_name(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    text = update.message.text
    context.user_data['name'] = text
    logger.info(f'{username=} {user_id=} вызвал функцию get_name')
    answer = [
        f'Твое имя - {text}'
    ]
    answer = '\n'.join(answer)
    update.message.reply_text(answer)

    return ask_surname(update, context)


def ask_surname(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    logger.info(f'{username=} {user_id=} вызвал функцию ask_surname')
    answer = [
        f'Назови свою фамилию'
    ]
    answer = '\n'.join(answer)
    update.message.reply_text(answer)

    return WAIT_SURNAME


def get_surname(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    text = update.message.text
    context.user_data['surname'] = text
    logger.info(f'{username=} {user_id=} вызвал функцию get_surname')
    answer = [
        f'Твоя фамилия - {text}'
    ]
    answer = '\n'.join(answer)
    update.message.reply_text(answer)

    return ask_birthday(update, context)


def ask_birthday(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    logger.info(f'{username=} {user_id=} вызвал функцию ask_birthday')
    answer = [
        f'Напиши свою дату рождения'
    ]
    answer = '\n'.join(answer)
    update.message.reply_text(answer)

    return WAIT_BIRTHDAY


def get_birthday(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    text = update.message.text
    context.user_data['birthday'] = text
    logger.info(f'{username=} {user_id=} вызвал функцию get_birthday')
    answer = [
        f'Твоя дата рождения - {text}'
    ]
    answer = '\n'.join(answer)
    update.message.reply_text(answer)

    return ask_sex(update, context)


def ask_sex(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    logger.info(f'{username=} {user_id=} вызвал функцию ask_sex')
    answer = [
        f'Назови свой пол'
    ]
    answer = '\n'.join(answer)
    update.message.reply_text(answer)

    return WAIT_SEX


def get_sex(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    text = update.message.text
    context.user_data['sex'] = text
    logger.info(f'{username=} {user_id=} вызвал функцию get_sex')
    answer = [
        f'Твой пол - {text}'
    ]
    answer = '\n'.join(answer)
    update.message.reply_text(answer)

    return ask_grade(update, context)


def ask_grade(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    logger.info(f'{username=} {user_id=} вызвал функцию ask_grade')
    answer = [
        f'Назови свой класс'
    ]
    answer = '\n'.join(answer)
    update.message.reply_text(answer)

    return WAIT_GRADE


def get_grade(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    text = update.message.text
    context.user_data['grade'] = text
    logger.info(f'{username=} {user_id=} вызвал функцию get_grade')
    answer = [
        f'Твой класс - {text}'
    ]
    answer = '\n'.join(answer)
    update.message.reply_text(answer)

    return register(update, context)


def register(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    logger.info(f'{username=} {user_id=} вызвал функцию register')
    name = context.user_data['name']
    surname = context.user_data['surname']
    birthday = context.user_data['birthday']
    sex = context.user_data['sex']
    grade = context.user_data['grade']
    write_to_db(user_id, name, surname, birthday, sex, grade)
    answer = [
        f'Привет!',
        f'Ты зареган!'
    ]
    answer = '\n'.join(answer)
    update.message.reply_text(answer)

    return ConversationHandler.END


register_handler = ConversationHandler(
    entry_points=[CommandHandler('register', check_register)],
    states={
        WAIT_NAME: [MessageHandler(Filters.text, get_name)],
        WAIT_SURNAME: [MessageHandler(Filters.text, get_surname)],
        WAIT_BIRTHDAY: [MessageHandler(Filters.text, get_birthday)],
        WAIT_SEX: [MessageHandler(Filters.text, get_sex)],
        WAIT_GRADE: [MessageHandler(Filters.text, get_grade)],
        WAIT_OK: [MessageHandler(Filters.text, get_yes_no)]
    },
    fallbacks=[]
)