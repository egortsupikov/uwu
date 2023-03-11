
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from telegram import Update
from config import TOKEN
from anecAPI import anecAPI



def start(update,context):
    update.message.reply_text('''привет я бот-слитый ботяра,
    как и ты ахахахха, я знаю команды /hello,/bye''')
    

def hello(update: Update ,context:CallbackContext):
    name = update.effective_user.first_name
    update.message.reply_animation('https://i.gifer.com/ICU.gif')
    update.message.reply_text(f'хыхыхыхыых,{name}!')


def bye(update,context):
    name = update.effective_user.full_name
    context.bot.send_photo(update.effective_chat.id,'https://avatars.mds.yandex.net/i?id=e03b27770aefb8780e693cac3754c232b347a73a-7066126-images-thumbs&n=13')
    context.bot.send_message(update.effective_chat.id,f'Пока,{name}!')


def get_numbers(update: Update ,context:CallbackContext):
    args = context.args
    if len(args) != 2:
        update.message.reply_text('ты чо нужно два числа ')
        return False
    num1 = is_number(args[0], update)
    num2 = is_number(args[1], update) if num1 != None else None
    if not num1 or not num2:
        update.message.reply_text('ты чо нужно числа вводить ')
        return False
    return num1, num2


def make_jokes(update: Update ,context:CallbackContext, ):
    message = update.message.text
    if 'штирлиц' in message.lower():
        update.message.reply_text(f'ты чмо не то что штирлиц')
    elif 'роналду' in message.lower():
        update.message.reply_text(f'suuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu')
    elif 'нов' in message.lower():
        update.message.reply_text(anecAPI.modern_joke())
    else:
        update.message.reply_text(f'я поймая сообщение: {message}' )




def plus(update: Update ,context:CallbackContext):
    if  get_numbers(update, context):
        num1, num2 = get_numbers(update, context)
        result = int(num1) + int(num2) 
        update.message.reply_text(result)


def minus(update: Update ,context:CallbackContext):
     if  get_numbers(update, context):
        num1, num2 = get_numbers(update, context)
        result = int(num1) - int(num2) 
        update.message.reply_text(result)

def mult(update: Update ,context:CallbackContext):
     if  get_numbers(update, context):
        num1, num2 = get_numbers(update, context)
        result = int(num1) * int(num2) 
        update.message.reply_text(result)

def div(update: Update ,context:CallbackContext):
     if  get_numbers(update, context):
        num1, num2 = get_numbers(update, context)
        result = int(num1) / int(num2) 
        update.message.reply_text(result)


def is_number(num, update):
    try:#попытайся выполнить этот код
        num = int(num)
        return num#вернет ничего
    except ValueError:#усли поймаешь ошибку 
        update.message.reply_text('чорт вводи числа ')
    


def sent_contact(update,context):
    update.message.reply_contact('88890009898','papy','dady')



def echo(update: Update ,context:CallbackContext):
    args = context.args

    update.message.reply_text('shsbxhsbxhsbhxbs')



updater = Updater(TOKEN)
dispatcher = updater.dispatcher


start_handler = CommandHandler('start',start)

hello_handler = CommandHandler('hello',hello)

bye_handler = CommandHandler('bye',bye)

contact_handler = CommandHandler('contact', sent_contact)

plus_handler = CommandHandler('plus', plus )

minus_handler = CommandHandler('minus', minus )

mult_handler = CommandHandler('mult', mult )

div_handler = CommandHandler('div', div)

joke_handler = MessageHandler(Filters.text, make_jokes)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(hello_handler)
dispatcher.add_handler(bye_handler)
dispatcher.add_handler(contact_handler)
dispatcher.add_handler(plus_handler)
dispatcher.add_handler(minus_handler)
dispatcher.add_handler(mult_handler)
dispatcher.add_handler(div_handler)
dispatcher.add_handler(joke_handler)
print('server started')
updater.start_polling()
updater.idle()


