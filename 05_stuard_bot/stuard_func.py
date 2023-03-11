from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler

EAT, DRINK, OLD = range(3) # шаги разговора
CHICKEN, FISH = 'курица', "рыба"
WATER, TEA, COFFEE, ALCOHOL = 'вода, чай, кофе, алкоголь'.split(', ')
YES, NO, NEXT = 'да', "нет", "дальше"


# [["курица"], ["рыба"], ["салат"]]


def start(update: Update, context: CallbackContext):
    mark_up= [[CHICKEN, FISH]]
    keyboard = ReplyKeyboardMarkup(mark_up,
                                     resize_keyboard=True,#чтобы кнопки поменьше
                                     one_time_keyboard=True#одноразовая
                                     )
    update.message.reply_text(
        'Приветствуем вас на борту! Что будете есть?',
        reply_markup=keyboard) #прикрепляем клавиатуру к сообщению
    return EAT


def what_eating(update: Update, context: CallbackContext):
    keyboard = [[WATER, TEA], [COFFEE, ALCOHOL]]
    markup_key = ReplyKeyboardMarkup(keyboard,
                                     resize_keyboard=True,
                                     one_time_keyboard=True
                                     )
    eat = update.message.text
    context.user_data['eat'] = eat #сохраняем в рюкзак
    update.message.reply_text(f'Что хотите пить',
                              reply_markup=markup_key)
    return DRINK


def what_drinking(update: Update, context: CallbackContext):
    drink = update.message.text
    context.user_data['drink'] = drink
    update.message.reply_text(f'Вы выбрали вариант "{drink}"',
                              reply_markup=ReplyKeyboardRemove())
    if drink == ALCOHOL:
        keyboard = [[YES, NO]]
        message = 'Есть ли вам 18?'
    else:
        keyboard = [[NEXT]]
        message = 'Нажмите кнопку "дальше" для завершения заказа'
    markup_key = ReplyKeyboardMarkup(keyboard,
                                     resize_keyboard=True,
                                     one_time_keyboard=True
                                     )
    update.message.reply_text(message, reply_markup=markup_key)
    return OLD


def how_old(update: Update, context: CallbackContext):
    print(3)
    answer = update.message.text
    context.user_data['answer'] = answer
    if answer == NO:
        update.message.reply_text(f'Вы не можете заказывать алкоголь. Давайте заново',
                                  reply_markup=ReplyKeyboardRemove())
        return start(update, context)
        

    update.message.reply_text(
        f'Итак, вы заказали следующее: {context.user_data["eat"]} и {context.user_data["drink"]}',
        reply_markup=ReplyKeyboardRemove())
    update.message.reply_text('Ожидайте заказ')
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('Значит, ты выбрал конец')
    return ConversationHandler.END
