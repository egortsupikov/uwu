from config import TOKEN
from telegram.ext import Updater,MessageHandler, Filters, ConversationHandler, CommandHandler
from function import * 
 

dialog_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        FIRST_NAME:[MessageHandler(Filters.text, get_name)],
        LAST_NAME:[MessageHandler(Filters.text & ~ Filters.command, get_last)],
        PATER_NAME:[MessageHandler(Filters.text & ~ Filters.command, get_pater)],
        AGE_NAME:[MessageHandler(Filters.text & ~ Filters.command, age_pater )]
    },
    fallbacks=[CommandHandler('end', end)]
)
    



updater = Updater(TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(dialog_handler)



print('приложение запущено')
updater.start_polling()
updater.idle()


