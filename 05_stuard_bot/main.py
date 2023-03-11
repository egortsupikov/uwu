from config import TOKEN
from telegram.ext import Updater,MessageHandler, Filters, ConversationHandler, CommandHandler
from stuard_func import * 
 

dialog_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        EAT:[MessageHandler(Filters.text & ~ Filters.command, what_eating)],
        DRINK:[MessageHandler(Filters.text & ~ Filters.command, what_drinking)],
        OLD:[MessageHandler(Filters.text & ~ Filters.command, how_old)]
        
    },
    fallbacks=[CommandHandler('end', cancel)]
)
    



updater = Updater(TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(dialog_handler)



print('приложение запущено')
updater.start_polling()
updater.idle()
