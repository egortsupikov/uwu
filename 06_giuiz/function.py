from telegram.ext import CallbackContext, ConversationHandler
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
import random
import csv

def read_csv():
    with open('06_giuiz\вопросы.csv','r', encoding='utf-8') as file:
        giuiz = csv.reader(file, delimiter='|')
        return giuiz
    

def write_csv():
    with open('06_giuiz\вопросы.csv','a', encoding='utf-8') as file:
        worker = csv.writer(file, delimiter='|',
                                        lineterminator ='\n')
        worker.writerow(['Какая столица Татарстана?',
                                    'Казань', 'Асьрана', 'Москва'])


def start(update: Update, context: CallbackContext):
    mark_up = [[GO]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=f'Нажми на кнопку "{GO}", поиграем!'
    )
    update.message.reply_sticker(START_STIKER)
    update.message.reply_text(
        ' Добро пожаловать')
    
    update.message.reply_text(
        f'Чтобы начать, нажми на "{GO}"', reply_markup=keyboard)
    return GAME









def end(update: Update, context: CallbackContext):  # точка выхода
    name = context.user_data['имя']
    update.message.reply_text(f"Значит, ты выбрал конец, {name}. Если хотите начать заново, нажмите /start")
    return ConversationHandler.END