from telegram.ext import CallbackContext, ConversationHandler
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
import random
import pymorphy2
from stiker import *

morph = pymorphy2.MorphAnalyzer()


NAME, BEGIN, LEVEL, GAME = range(4)
GO = "Вперед"
SKIP = "Пропустить"
EASY, MEDIUM, HARD = "Простой", "Средний", "Сложный"


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
        'В этой игре компьютер загадывает слово, и говорит тебе, сколько в нем букв')
    update.message.reply_text('Ты говоришь слово из такого же количества букв')
    update.message.reply_text(
        'Если у какой-то из букв твоего совпадает позиция с буквой из загаданного слова - это бык')
    update.message.reply_text(
        'Если просто такая буква есть в слове - это корова')
    update.message.reply_text("Твоя цель - отгадать загаданное слово")
    update.message.reply_text(
        f'Чтобы начать, нажми на "{GO}"', reply_markup=keyboard)
    return NAME

def get_name(update: Update, context: CallbackContext):
    mark_up = [[SKIP]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    full_name = update.effective_chat.full_name
    update.message.reply_text(f"Можно называть вас {full_name}? Если нет, то введите свое имя, иначе - нажмите {SKIP}", reply_markup=keyboard)
    return BEGIN

def begin(update: Update, context: CallbackContext):
    name = update.message.text
    if name == SKIP:
        name = update.effective_chat.full_name
    context.user_data['имя'] = name
    mark_up = [[EASY, MEDIUM, HARD]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=f'{EASY} - 3 буквы, {MEDIUM} - 4 буквы, {HARD} - 5 букв'
    )
    update.message.reply_text(f'Выбери уровень сложности, {name}, или нажми /end!', reply_markup=keyboard)
    # если ключа "секретное число" нет в рюкзаке
    # secret_number = random.randint(1000, 9999)
    # context.user_data['секретное число'] = secret_number
    # update.message.reply_text('Я загадал число, отгадай или нажми /end!')
    # создается "секретное число" в рюкзаке
    return LEVEL

def level(update: Update, context: CallbackContext):
    level_storage = update.message.text #ответ пользователя
    name = context.user_data['имя'] #извлекаем имя 
    if level_storage == EASY:
        with open("02_cows_and_bulls/easy.txt", encoding="utf-8") as file:
            words = file.read().split("\n")
    elif level_storage == MEDIUM:
        with open("02_cows_and_bulls/medium.txt", encoding="utf-8") as file:
            words = file.read().split("\n")
    elif level_storage == HARD:
        with open("02_cows_and_bulls/hard.txt", encoding="utf-8") as file:
            words = file.read().split("\n")
    else:
        update.message.reply_text(f"{name}, этот файл недоступен")
    word = random.choice(words)
    context.user_data["word"] = word
    update.message.reply_text(f'{name}, отгадайте мое слово. Количество букв в нем -  {len(word)}.')
    return GAME
    


def game(update: Update, context: CallbackContext):  # callback'
    my_word = update.message.text.lower()
    tag = morph.parse(my_word)[0]
    secret_word = context.user_data['word']  # достаем из рюкзака
    update.message.sticker
    
    if len(my_word) != len(secret_word) and not my_word.isalpha():
        update.message.reply_text(f"Нужно вводить слова из {len(secret_word)} букв")
        return  # выход из функции
    elif my_word != tag.normal_form or tag.tag.POS != 'NOUN'  or 'DictionaryAnalyzer()' not in str(tag.methods_stack):
        # если не начальная форма и не существительное
        update.message.reply_text(f"Нужно вводить НОРМАЛЬНЫЕ слова из {len(secret_word)} букв")
        return
    cows = 0
    bulls = 0
    for mesto, letter in enumerate(my_word):
        if letter in secret_word:
            if my_word[mesto] == secret_word[mesto]:
                bulls += 1
            else:
                cows += 1
    update.message.reply_text(f'В вашем слове {cows} коров и {bulls} быков')
    if bulls == len(secret_word):
        update.message.reply_text('Вы угадали! Вы красавчик. Если хотите начать заново, нажмите /start')
        del context.user_data['word']

def end(update: Update, context: CallbackContext):  # точка выхода
    name = context.user_data['имя']
    update.message.reply_text(f"Значит, ты выбрал конец, {name}. Если хотите начать заново, нажмите /start")
    return ConversationHandler.END