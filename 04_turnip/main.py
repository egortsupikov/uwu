from config import TOKEN
from telegram.ext import (
    Updater,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    Filters
    )
from function import *

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        BEGIN: [MessageHandler(Filters.text & ~Filters.command, begin)],
        GAME: [MessageHandler(Filters.text & ~Filters.command, game)]
    },
    fallbacks=[CommandHandler('end', end)]
)


updater = Updater(TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(conv_handler)

print('Сервер запущен!')
updater.start_polling()
updater.idle() #ctrl + c


