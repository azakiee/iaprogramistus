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


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def ask_name(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    name = update.message.from_user.name
    text = update.message.text
    logger.info(f'{user_id=} Bызвaл функцию ask_name')
    text = f'Твоё имя - {text}'


def get_name(update: Update, context: CallbackContext):
    pass


def ask_surname(update: Update, context: CallbackContext):
    pass


def get_surname(update: Update, context: CallbackContext):
    pass


def ask_birthday(update: Update, context: CallbackContext):
    pass


def get_birthday(update: Update, context: CallbackContext):
    pass


def register(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    name = update.message.from_user.name
    logger.info(f'{user_id=} Bызвaл функцию register')
    answer = [
        f'Привет!'
        f'Зарегистрировал тебя!'
    ]
    answer = '\n'.join(answer)
    update.message.reply_text(answer)

    return ConversationHandler.END
