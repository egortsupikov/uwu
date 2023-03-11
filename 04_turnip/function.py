from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import pymorphy2

morph = pymorphy2.MorphAnalyzer()
BEGIN, GAME = 1, 2
GO = "Вперед"


def start(update: Update, context: CallbackContext):
    mark_up = [[GO]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard = True,
        input_field_placeholder = f'Нажми на кнопку "{GO}", путник!'
    )
    update.message.reply_text(
        f"""
        Ты любишь придумывать сказки? 
        Я очень люблю. Ты знаешь сказку как посадил дед репку?
        А кто помогал деду репку тянуть? Чтобы начать, нажми на кнопку {GO}!
        """,
        reply_markup=keyboard)
    return BEGIN


def begin(update: Update, context: CallbackContext):  # первый шаг разговора
    heroes = [["дедку"], ["дедка", "репку"]]
    context.user_data["heroes"] = heroes # сохраняем в словарь 
    update.message.reply_text('''
                            Посадил дед репку. Выросла репка большая-пребольшая.
                            Стал дед репку из земли тянуть. 
                            Тянет-потянет - вытянуть не может.
                            Кого позвал дедка?
                            ''', reply_markup=ReplyKeyboardRemove())
    return GAME


    


def end(update: Update, context: CallbackContext):  # точка выхода
    update.message.reply_text("Значит, ты выбрал конец")
    return ConversationHandler.END


def game(update: Update, context: CallbackContext):
    text = update.message.text
    text = morph.parse(text)[0] # тег
    if text.tag.animacy == "anim": # если одушевленный
        nomn = text.inflect({'nomn'}).word  # именительный падеж
        accs = text.inflect({'accs'}).word  # винительный падеж
        heroes = context.user_data["heroes"] # достаем из рюкзака
        heroes[0].insert(0, nomn) # бабка за дедку
        heroes.insert(0, [accs]) 
        answer = f"Я {nomn}. Буду помогать. "      
        for nom, acc in heroes[1:]: 
            answer += f"{nom} за {acc}. "
        answer += "Тянут-потянут - вытянуть не могут. Кого позовем еще?"    
        update.message.reply_text(f'{answer}')
    else: #если персонаж неодушевленный 
        update.message.reply_text(f'Долго искали мы {text.normal_form}: ничего не нашли')


