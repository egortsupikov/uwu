from config import TOKEN
from telegram.ext import (
    Updater,
    Filters,
    MessageHandler,
    CommandHandler,
    ConversationHandler
)
from function import *


updater = Updater(TOKEN)
dispatcher = updater.dispatcher

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
          NAME: [MessageHandler(Filters.regex(f"^({GO})$"), get_name)],
          BEGIN: [MessageHandler(Filters.text & ~Filters.command, begin)],
          LEVEL: [MessageHandler(Filters.regex(f"^({EASY}|{MEDIUM}|{HARD})$"), level)],
          GAME: [MessageHandler(Filters.text & ~Filters.command, game)]  
        },
    fallbacks=[CommandHandler('end', end)]
)


dispatcher.add_handler(conv_handler)

print('Сервер запущен!')
updater.start_polling()
updater.idle()  # ctrl + C
