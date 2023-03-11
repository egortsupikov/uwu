from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update

FIRST_NAME = 1
LAST_NAME = 2
PATER_NAME = 3
AGE_NAME = 4


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Пазговор начался.Скажи свои данные паспота.')
    update.message.reply_text('Как тебя зовут?.')
    return FIRST_NAME


def get_name(update: Update, context: CallbackContext):
    name = update.message.text
    context.user_data['name'] = name
    update.message.reply_text(f'вы ввели имя {name}')
    update.message.reply_text('Назови мне свое фамилию')

    return LAST_NAME


def get_last(update: Update, context: CallbackContext):
    last_name = update.message.text
    context.user_data['last_name'] = last_name
    update.message.reply_text(f'вы ввели фамилию {last_name}')
    update.message.reply_text('Назови свое отчество')
    return PATER_NAME


def get_pater(update: Update, context: CallbackContext):
    pater_name = update.message.text
    context.user_data['pater_name'] = pater_name
    update.message.reply_text(f'вы ввели отчество {pater_name}')
    update.message.reply_text(f'назови свой возраст {pater_name}')
    return AGE_NAME


def age_pater(update: Update, context: CallbackContext):
    age_name = update.message.text
    if not age_name.isdigit():
        update.message.reply_text('вы ввели не число')
        return None
    age_name = int(age_name)
    if age_name > 140:
        update.message.reply_text('Староват для телеги')
        return None
    age_name = update.message.text
    context.user_data['age_name'] = age_name
    update.message.reply_text(f'вы ввели возраст {age_name}')
    return ConversationHandler.END


def end(update: Update, context: CallbackContext):
    update.message.reply_text('Сбор данных прерван')
    return ConversationHandler.END
