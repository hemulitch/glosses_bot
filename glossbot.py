import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot('5376935937:AAE3l_wfQ_h-EbCkj3JZP8MAnOpLoikNcR4')

@bot.message_handler(commands=['start', 'help'],content_types=['text'])
def get_text_messages(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, 'Привет! Я glosses_bot, и моя основная функция - глоссирование слов. Я пока умею не так много, но обязательно научусь делать больше в ближайшее время! \n\nЧто такое глосса?\nЭто способ указания на грамматические характеристики отдельной словоформы: сокращенная запись значений грамматических признаков, обычно помещается под соответствующей формой.\n\nТак, например, глоссы для слова "красивую" будут выглядеть так: \nкрасивую\nкрасивый-ACC.F\n\nЧтобы начать работу, отправь мне слово для глоссирования.')
        bot.register_next_step_handler(message, get_word)
    elif message.text == '/help':
        bot.send_message(message.from_user.id, 'Чтобы начать глоссирование, напиши /start')

def get_word(message): #получаем слово и проверяем, является ли полученное словом
    global word
    if ' ' in message.text: #проверяем, что слово написано без пробелов ("ко ты" не является словом, "коты" - является)
            bot.send_message(message.from_user.id, 'Напиши, пожалуйста, одно слово без пробелов')
    else:
            break_count = 0 #проверяем, что слово написано кириллицей
            for symbol in message.text:
                if symbol.lower() in 'абвгдеёжзийклмнопрстуфхцчшщэюяъьы-':
                    break_count +=1 
            if break_count == len(message.text): #получаем слово в начальной форме
                word = message.text
                bot.send_message(message.from_user.id, 'Напиши это слово в начальной форме.')
                bot.register_next_step_handler(message, get_pos)
            else:
                bot.send_message(message.from_user.id, 'Слово должной быть написано кириллицей, без использования специальных символов или других систем графики!')
                bot.register_next_step_handler(message, get_word)

def get_pos(message): #получаем часть речи слова
    global word_initial
    word_initial = message.text
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Существительное", callback_data="NOUN"),
               InlineKeyboardButton("Глагол", callback_data="VERB"),
               InlineKeyboardButton("Прилагательное", callback_data="ADJ"),
               InlineKeyboardButton("Местоимение", callback_data="PRONOUN"),
               InlineKeyboardButton("Наречие", callback_data="ADV"),
               InlineKeyboardButton("Частица", callback_data="PARTICIPLE"),
               InlineKeyboardButton("Союз", callback_data="CONJ"),
               InlineKeyboardButton("Предлог", callback_data="PREP"),
               InlineKeyboardButton("Причастие", callback_data="PART"),
               InlineKeyboardButton("Деепричастие", callback_data="CVB"))
    bot.send_message(message.from_user.id,
                     text="Спасибо, запомнил! А какая часть речи у этого слова?\n\n(От части речи слова зависит набор необходимых мне глосс)",
                     reply_markup=markup)

    
@bot.callback_query_handler(func=lambda call: call.data in ['NOUN', 'VERB','ADJ','PRONOUN','ADV','PARTICIPLE','CONJ','PREP','PART','CVB'])
def get_pos2(call): #отправляем слово в функции для различных грамматических характеристик в зависимости от части речи
    global pos
    pos = call.data
    if pos == "NOUN":
        get_case(call)
    elif pos == "VERB":
        get_modul(call)
    elif pos == "ADV" or pos == "ADJ":
        get_comparison(call)
    elif pos in ['CONJ','PREP','PARTICIPLE']:
        bot.edit_message_text(chat_id=call.message.chat.id, 
                              message_id=call.message.message_id, 
                              text=f"{word}\n{word_initial}\n\nГотово!\n\nОбычно глоссы для частиц, союзов и предлогов в русском оформляются либо падежом:\n\nв (Москву)\nALL\n\nлибо переводом:\n\n\n\nв (Москву)\nto\n\nЯ пока этого не умею, но обязательно научусь!",
                              reply_markup=None)
    elif pos == "CVB":
        get_tense(call)
    elif pos == "PART":
        get_tense(call)
    elif pos == "PRONOUN":
        get_pronoun_type(call)

#функция для определения разряда местоимения (важно для грам. характеристик местоимения)
@bot.callback_query_handler(func=lambda call: call.data in ['PRONOUN'])
def get_pronoun_type(call):
    markup_type = InlineKeyboardMarkup()
    markup_type.add(InlineKeyboardButton("Личный", callback_data="PERS"),
                    InlineKeyboardButton("Притяжательный", callback_data="POSS"),
                    InlineKeyboardButton("Возвратный", callback_data="REFL"),
                    InlineKeyboardButton("Вопросительно-относительный", callback_data="REL"),
                    InlineKeyboardButton("Указательный", callback_data="DEM"),
                    InlineKeyboardButton("Определительный", callback_data="DEF"),
                    InlineKeyboardButton("Неопределенный", callback_data="INDEF"),
                    InlineKeyboardButton("Отрицательный", callback_data="NEG"))
    bot.edit_message_text(chat_id=call.message.chat.id, 
                          message_id=call.message.message_id, 
                          text="А какой разряд местоимения? \n\nРазряд местоимений не обозначается в глоссах, но он поможет мне лучше обработать твое слово :)",
                          reply_markup=markup_type)

# функция для определения степени сравнения прилагательных и наречий
@bot.callback_query_handler(func=lambda call: call.data in ['ADJ','ADV'])
def get_comparison(call):
    markup_comparison = InlineKeyboardMarkup()
    markup_comparison.add(InlineKeyboardButton("Положительная", callback_data="POS"), 
                          InlineKeyboardButton("Сравнительная", callback_data="COMP"),
                          InlineKeyboardButton("Превосходная", callback_data="SUPERL"))
    bot.edit_message_text(chat_id=call.message.chat.id, 
                          message_id=call.message.message_id, 
                          text="А какая степень сравнения?\n\nДля степеней сравнения существуют такие глоссы: \n— COMP для сравнительной степени (лучше, красивее);\n— SUPERL для превосходной степени (самый красивый, красивейший)\n— Положительная степень никак не обозначается",
                          reply_markup=markup_comparison)

        
#функция для определения наклонения глагола       
@bot.callback_query_handler(func=lambda call: call.data in ['VERB'])
def get_modul(call):
    markup_modul = InlineKeyboardMarkup()
    markup_modul.add(InlineKeyboardButton("Изъявительное", callback_data="IND"),
                         InlineKeyboardButton("Повелительное", callback_data="IMP"),
                         InlineKeyboardButton("Условное", callback_data="CON"))
    bot.edit_message_text(chat_id=call.message.chat.id, 
                          message_id=call.message.message_id, 
                          text="А какое наклонение? \n\nДля наклонения глагола существуют такие глоссы:\n— IND для изъявительного наклонения (его еще называют индикативом); \n— IMP для повелительного наклонения, оно же императив;\n— COND для условного наклонения - кондиционалиса (но я пока не умею обрабатывать условное наклонение... Скоро научусь, правда!) ",
                          reply_markup=markup_modul)

#функция для определения времени глагола
@bot.callback_query_handler(func=lambda call: call.data in ['IND','CVB','PART'])
def get_tense(call):
    global modul
    if pos == 'VERB':
        modul = call.data
    markup_tense = InlineKeyboardMarkup()
    markup_tense.add(InlineKeyboardButton('Прошедшее', callback_data="PST"),
                     InlineKeyboardButton('Настоящее', callback_data="PRS"),
                     InlineKeyboardButton('Будущее', callback_data="FUT"))
    bot.edit_message_text(chat_id=call.message.chat.id, 
                          message_id=call.message.message_id, 
                          text=f"{word}\n{word_initial}\n\nА какое время?\n\n Для времени существуют следующие глоссы: \n— PST для прошедшего (past) времени;\n— PRS для настоящего (presens) времени;\n— FUT для будущего (future) времени",
                          reply_markup=markup_tense)

#функция для определения залога причастия
@bot.callback_query_handler(func=lambda call: call.data in ['PRS','PST'])
def get_voice(call):
    global tense
    if pos == 'PART':
        tense = call.data
        markup_voice = InlineKeyboardMarkup()
        markup_voice.add(InlineKeyboardButton("Активный", callback_data="ACT"), 
                          InlineKeyboardButton("Пассивный", callback_data="PASS"))
        bot.edit_message_text(chat_id=call.message.chat.id, 
                              message_id=call.message.message_id, 
                              text=f"{word}\n{word_initial}-{tense}\n\nА какой залог? \n\n Для залога существуют следующие глоссы:\n— PASS для пассивного залога;\n— Активный залог в глоссах никак не обозначается;",
                              reply_markup=markup_voice)
    elif pos == "VERB": #перенаправляем в др функцию, иначе программа остановится
        get_number(call)
    elif pos == "CVB": #перенаправляем в др функцию, иначе программа остановится
        get_number(call)



#функция для определения формы причастий, прилагательных
@bot.callback_query_handler(func=lambda call: call.data in ['POS','COMP','SUPERL','ACT','PASS'])
def get_form(call):
    global voice
    global comparison
    explain_form = "От этого зависит набор глосс:\n— Полная форма: падеж, число, род;\n— Краткая форма: число, род, а падеж всегда один - именительный;"
    comparison = call.data
    if pos == "ADV":
        if comparison == "POS":
            bot.edit_message_text(chat_id=call.message.chat.id, 
                                  message_id=call.message.message_id, 
                                  text=f"{word}\n{word_initial}\n\nГотово!",
                                  reply_markup=None)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, 
                                  message_id=call.message.message_id, 
                                  text=f"{word}\n{word_initial}-{comparison}\n\nГотово!",
                                  reply_markup=None)
    elif pos == "ADJ":
        if comparison == "POS":
            markup_form = InlineKeyboardMarkup()
            markup_form.add(InlineKeyboardButton("Полная", callback_data="FULL"),
                            InlineKeyboardButton("Краткая", callback_data="SHORT"))
            bot.edit_message_text(chat_id=call.message.chat.id, 
                                  message_id=call.message.message_id, 
                                  text=f"А какая форма?\n\n{explain_form}",
                                  reply_markup=markup_form)     
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, 
                                  message_id=call.message.message_id, 
                                  text=f"{word}\n{word_initial}-{comparison}\n\nГотово!",
                                  reply_markup=None)
    elif pos == "PART":
        voice = call.data
        markup_form = InlineKeyboardMarkup()
        markup_form.add(InlineKeyboardButton("Полная", callback_data="FULL"),
                        InlineKeyboardButton("Краткая", callback_data="SHORT"))
        if voice == "ACT":
            bot.edit_message_text(chat_id=call.message.chat.id, 
                                  message_id=call.message.message_id, 
                                  text=f"{word}\n{word_initial}-{tense}\n\nА какая форма?\n\n{explain_form}",
                                  reply_markup=markup_form)     
        elif voice == "PASS":
            bot.edit_message_text(chat_id=call.message.chat.id, 
                                  message_id=call.message.message_id, 
                                  text=f"{word}\n{word_initial}-{tense}.{voice}\n\nА какая форма?\n\n{explain_form}",
                                  reply_markup=markup_form)     


#функция для определения падежа                    
@bot.callback_query_handler(func=lambda call: call.data in ['NOUN','FULL',"PERS","POSS","REL","DEM","DEF","INDEF","NEG"])  
def get_case(call):
        global pro_type
        global form
        explain_case = "Падежей очень много... В русском выделяют примерно шесть.\n\nNOM - именительный падеж. Вопросы: 'кто?', 'что?'. Обычно падеж кодируется как агенс. Слова, которые обозначаются этим падежом, зачастую в предложении являются подлежащими.\n\nGEN - родительный падеж. Отвечает на вопросы 'кого?', 'чего?'. Имеет три функции: 1) притяжательная: день котика; 2) разделительная: немного котика; 3) отложительная: уберечься от котика.\n\nDAT - дательный падеж. Отвечает на вопросы 'кому?', 'чему?'. Используется с глаголами, выражающими действие, направленное к этому предмету и производным от него.\n\nACC - винительный падеж. Отвечает на вопросы 'кого?', 'что?'. Обозначает объект действия (прямое дополнение).\n\nINS - творительный падеж. Отвечает на вопросы 'кем?', 'чем?'. Выражает такие семантические роли: \n1) инструмент: бить котиком;\n2) средство: рисовать котиком;\n3) пациенс (объект, претерпевающий наибольшие изменения в ходе действия) и объект обладания: обладать котиком;\n4) агенс: дом строится котиком;\n5) эффектор: котиком сорвало крышу;\n6) причина: болеть котиком;\n7) траектория: ехать котиком;\n8) стимул: восхищаться котиком;\n9) время: зимним котиком;\n10) мера: грузить котиком;\n11) аспект: богат котиком;\n12) эталон сравнения и ориентация: кричать котиком;\n13) отправная, промежуточная и конечная точка: закончиться котиком.\n\nPREP - предложный падеж... Все сложно. В русском он отвечает на вопросы 'о ком?', 'о чем?', и иногда имеет значение локатива (глосса LOC). Я пока не умею их различать, но научусь!"
        if pos == "ADJ" or pos == "PART":
            form = call.data
        elif pos == "PRONOUN":
            pro_type = call.data
                
        markup_case = InlineKeyboardMarkup()
        markup_case.add(InlineKeyboardButton("Именительный", callback_data="NOM"),
            InlineKeyboardButton("Родительный", callback_data="GEN"),
            InlineKeyboardButton("Винительный", callback_data="ACC"),
            InlineKeyboardButton("Дательный", callback_data="DAT"),
            InlineKeyboardButton("Творительный", callback_data="INS"),
            InlineKeyboardButton("Местный", callback_data="PREP"))
        
        if pos == "ADJ" or "PRONOUN":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                  text=f"А какой падеж?\n\n{explain_case}",
                                  reply_markup=markup_case)
        elif pos == "PART":
            if voice == "ACT":
                bot.edit_message_text(chat_id=call.message.chat.id, 
                                      message_id=call.message.message_id, 
                                      text=f"{word}\n{word_initial}-{tense}\n\nА какой падеж?\n\n{explain_case}",
                                      reply_markup=markup_case)
            elif voice == "PASS":
                bot.edit_message_text(chat_id=call.message.chat.id, 
                                      message_id=call.message.message_id, 
                                      text=f"{word}\n{word_initial}-{tense}.{voice}\n\nА какой падеж?\n\n{explain_case}",
                                      reply_markup=markup_case)
 


#функция для определения числа
@bot.callback_query_handler(func=lambda call: call.data in ['NOM', 'GEN','ACC','DAT','INS','PREP','IMP','PST','PRS','FUT','SHORT'])
def get_number(call):
    global case
    global modul
    global tense
    global form
    explain_number = "Для этой грамматической характеристики существуют такие глоссы как...\n— SG для единственного числа (грамматический разряд, показывающий, что речь идет об одном предмете, лице); \n— PL для множественного числа (грамматическое число, используемое при обозначении нескольких предметов, объединенных по какому-либо признаку (однородных предметов);"
    if pos == "NOUN":
        case = call.data
    elif pos == "ADJ" or pos == "PART":
        if call.data == "SHORT":
            form = call.data
        else:
            case = call.data
    elif pos == "VERB" or pos == "CVB":
        if call.data != "IMP":
            tense = call.data
            if pos == "CVB":
                bot.edit_message_text(chat_id=call.message.chat.id, 
                                      message_id=call.message.message_id, 
                                      text=f"{word}\n{word_initial}-{pos}.{tense}\n\nГотово!",
                                      reply_markup=None)
        else:
            modul = call.data
    elif pos == "PRONOUN":
        case = call.data
        if (pro_type == 'REFL'):
            get_ready(call)
    if (word_initial.lower() in ['сколько', 'кто', 'что', 'несколько', 'нисколько', 'никто','ничто', 'столько', 'некто', 'нечто']):
            get_ready(call)
    
    markup_number = InlineKeyboardMarkup()
    markup_number.add(InlineKeyboardButton("Единственное", callback_data="SG"),
                      InlineKeyboardButton("Множественное", callback_data="PL"))
    
    if pos == "NOUN" or pos == "PRONOUN":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                              text=f"{word}\n{word_initial}-{case}\n\nА какое число?\n\n{explain_number}",
                              reply_markup=markup_number)
    elif pos == "ADJ":
        if form == "FULL":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                  text=f"{word}\n{word_initial}-{case}\n\nА какое число?\n\n{explain_number}",
                                  reply_markup=markup_number)
        elif form == "SHORT":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                  text=f"{word}\n{word_initial}\n\nА какое число?\n\n{explain_number}",
                                  reply_markup=markup_number)
    elif pos == "PART":
        if form == "FULL":
            if voice == "ACT":
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                      text=f"{word}\n{word_initial}-{tense}-{case}\n\nА какое число?\n\n{explain_number}",
                                      reply_markup=markup_number)
            elif voice == "PASS":
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                      text=f"{word}\n{word_initial}-{tense}.{voice}-{case}\n\nА какое число?\n\n{explain_number}",
                                      reply_markup=markup_number)
        elif form == "SHORT":
            if voice == "ACT":
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                      text=f"{word}\n{word_initial}-{tense}\n\nА какое число?\n\n{explain_number}",
                                      reply_markup=markup_number)
            elif voice == "PASS":
                 bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                       text=f"{word}\n{word_initial}-{tense}.{voice}\n\nА какое число?\n\n{explain_number}",
                                       reply_markup=markup_number)
    elif pos == "VERB":
        if modul == "IMP":
             bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                   text=f"{word}\n{word_initial}-{modul}\n\nА какое число?\n\n{explain_number}",
                                   reply_markup=markup_number)
        elif modul == "IND":
             bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                   text=f"{word}\n{word_initial}-{tense}\n\nА какое число?\n\n{explain_number}",
                                   reply_markup=markup_number)


#функция для определения лица глаголов и личных местоимений
@bot.callback_query_handler(func=lambda call: call.data in ['SG','PL'])
def get_person(call):
    global number
    global case
    explain_person = "Лицо — грамматическая категория, выражающая отношения участников описываемой ситуации и участников речевого акта. Для этой категории существуют глоссы...\n\n1 - первое лицо (говорящий или группа, в которую он входит: я, мы);\n2 - второе лицо (слушающий или группа, в которую он входит: ты, вы);\n3 - третье лицо (участник, не являющийся ни говорящим, ни слушающим: он, она, оно, они);"
    if pos == "VERB":
        if modul == "IND":
            if tense != "PST":
                number = call.data
                markup_person = InlineKeyboardMarkup()
                markup_person.add(InlineKeyboardButton('1-е лицо', callback_data="1"),
                                  InlineKeyboardButton('2-е лицо', callback_data="2"),
                                  InlineKeyboardButton('3-е лицо', callback_data="3"))
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                      text=f"{word}\n{word_initial}-{tense}.{number}\n\nА какое лицо?\n\n{explain_person}",
                                      reply_markup=markup_person)
            else:
                get_gender(call)
        
    elif pos == "PRONOUN": 
        number = call.data
        if pro_type == "PERS":
            markup_person = InlineKeyboardMarkup()
            markup_person.add(InlineKeyboardButton('1-е лицо', callback_data="1"),
                              InlineKeyboardButton('2-е лицо', callback_data="2"),
                              InlineKeyboardButton('3-е лицо', callback_data="3"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                  text=f"{word}\n{word_initial}-{case}\n\nА какое лицо?\n\n{explain_person}",
                                  reply_markup=markup_person)
        else:
            get_gender(call)
    elif pos == "ADJ":
        get_gender(call)
    
    else:
        get_ready(call)
        

#функция для определения рода
@bot.callback_query_handler(func=lambda call: call.data in ['SG','PL','1','2','3'])
def get_gender(call):
    global number
    global person
    global case
    explain_gender = "Род — категория, представляющая распределение слов и форм по классам, традиционно соотносимым с признаками пола или их отсутствием. В русском языке для описания категории рода используют три глоссы:\n— F для женского рода;\n— M для мужского рода; \n— N для среднего рода;"
    if (pos == "VERB" and modul == "IND" and tense == "PST") or pos == "ADJ" or pos == "PART":
        number = call.data
        if number == "PL":
            if pos == "VERB":             
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                      text=f"{word}\n{word_initial}-{tense}-{number}\n\nГотово!",
                                      reply_markup=None)
            elif pos == "ADJ":
                if form == "SHORT":
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                          text=f"{word}\n{word_initial}-{number}\n\nГотово!",
                                          reply_markup=None)
                else:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                          text=f"{word}\n{word_initial}-{case}.{number}\n\nГотово!",
                                          reply_markup=None)
            elif pos == "PART":
                if form == "FULL":
                    if voice == "ACT":
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                              text=f"{word}\n{word_initial}-{tense}-{case}.{number}\n\nГотово!",
                                              reply_markup=None)
                    elif voice == "PASS":
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                              text=f"{word}\n{word_initial}-{tense}.{voice}-{case}.{number}\n\nГотово!",
                                              reply_markup=None)
                elif form == "SHORT":
                    if voice == "ACT":
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                              text=f"{word}\n{word_initial}-{tense}-{number}\n\nГотово!",
                                              reply_markup=None)
                    elif voice == "PASS":
                         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                               text=f"{word}\n{word_initial}-{tense}.{voice}-{number}\n\nГотово!",
                                               reply_markup=None)
        else:
            markup_gender = InlineKeyboardMarkup()
            markup_gender.add(InlineKeyboardButton('Женский', callback_data="F"),
                              InlineKeyboardButton('Средний', callback_data="N"),
                              InlineKeyboardButton('Мужской', callback_data="M"))
            if pos == "VERB":
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                      text=f"{word}\n{word_initial}-{tense}\n\nА какой род?\n\n{explain_gender}",
                                      reply_markup=markup_gender)  
            elif pos == "ADJ":
                if form == "SHORT":
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                          text=f"{word}\n{word_initial}\n\nА какой род?\n\n{explain_gender}",
                                          reply_markup=markup_gender)
                else:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                          text=f"{word}\n{word_initial}-{case}\n\nА какой род?\n\n{explain_gender}",
                                          reply_markup=markup_gender)
            elif pos == "PART":
                if form == "FULL":
                    if voice == "ACT":
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                              text=f"{word}\n{word_initial}-{tense}-{case}\n\nА какой род?\n\n{explain_gender}",
                                              reply_markup=markup_gender)
                    elif voice == "PASS":
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                              text=f"{word}\n{word_initial}-{tense}.{voice}-{case}\n\nА какой род?\n\n{explain_gender}",
                                              reply_markup=markup_gender)
                elif form == "SHORT":
                    if voice == "ACT":
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                              text=f"{word}\n{word_initial}-{tense}\n\nА какой род?\n\n{explain_gender}",
                                              reply_markup=markup_gender)
                    elif voice == "PASS":
                         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                               text=f"{word}\n{word_initial}-{tense}.{voice}\n\nА какой род?\n\n{explain_gender}",
                                               reply_markup=markup_gender)
    elif pos == "PRONOUN":
        if pro_type == "PERS":
            person = call.data
            if person == "2" or person == "1":
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                      text=f"{word}\n{word_initial}-{person}{number}.{case}\n\nГотово!",
                                      reply_markup=None)
            elif person == "3" and number == "PL":
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                      text=f"{word}\n{word_initial}-{person}{number}.{case}\n\nГотово!",
                                      reply_markup=None)
        else:
            if number == "PL":
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                      text=f"{word}\n{word_initial}-{case}.{number}\n\nГотово!",
                                      reply_markup=None)
        if (pro_type == "PERS" and person == "3" and number == "SG") or (pro_type != "PERS" and number == "SG"):
            markup_gender = InlineKeyboardMarkup()
            markup_gender.add(InlineKeyboardButton('Женский', callback_data="F"),
                              InlineKeyboardButton('Средний', callback_data="N"),
                              InlineKeyboardButton('Мужской', callback_data="M"))
            if pro_type == "PERS":
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                      text=f"{word}\n{word_initial}-{person}{number}.{case}\n\nА какой род?\n\n{explain_gender}",
                                      reply_markup=markup_gender)
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                      text=f"{word}\n{word_initial}-{case}\n\nА какой род?\n\n{explain_gender}",
                                      reply_markup=markup_gender)
            
    elif pos == "VERB" and (modul == "IMP" or tense != "PST"):
        get_ready(call)
    else:
        get_person(call)



#функция для вывода всего, что не вывелось раньше
@bot.callback_query_handler(func=lambda call: call.data in ['SG','PL','F','M','N','1','2','3'])
def get_ready(call):
    global number
    global gender
    global person
    if pos == "NOUN":
        number = call.data
        if number == "PL":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                  text=f"{word}\n{word_initial}-{case}.{number}\n\nГотово!", 
                                  reply_markup=None)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                  text=f"{word}\n{word_initial}-{case}\n\nГотово!",
                                  reply_markup=None)
    elif pos == "VERB":
        if modul == "IMP":
            number = call.data
            if number == "PL":
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                      text=f"{word}\n{word_initial}-{modul}.{number}\n\nГотово!", 
                                      reply_markup=None)
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                      text=f"{word}\n{word_initial}-{modul}\n\nГотово!",
                                      reply_markup=None)
        elif modul == "IND":
            if tense == "PST":
                gender = call.data
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                      text=f"{word}\n{word_initial}-{tense}-{gender}\n\nГотово!",
                                      reply_markup=None)
            else:
                person = call.data
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                      text=f"{word}\n{word_initial}-{tense}.{person}{number}\n\nГотово!",
                                      reply_markup=None)
    elif pos == "ADJ":
        gender = call.data
        if form == "SHORT":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                  text=f"{word}\n{word_initial}-{gender}\n\nГотово!",
                                  reply_markup=None)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                  text=f"{word}\n{word_initial}-{case}.{gender}\n\nГотово!",
                                  reply_markup=None)
    elif pos == "PART":
        gender = call.data
        if form == "FULL":
            if voice == "ACT":
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                      text=f"{word}\n{word_initial}-{tense}-{case}.{gender}\n\nГотово!",
                                      reply_markup=None)
            elif voice == "PASS":
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                      text=f"{word}\n{word_initial}-{tense}.{voice}-{case}.{gender}\n\nГотово!",
                                      reply_markup=None)
        elif form == "SHORT":
            if voice == "ACT":
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                      text=f"{word}\n{word_initial}-{tense}-{gender}\n\nГотово!",
                                      reply_markup=None)
            elif voice == "PASS":
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                      text=f"{word}\n{word_initial}-{tense}.{voice}-{gender}\n\nГотово!",
                                      reply_markup=None)
    elif pos == "PRONOUN":
        gender = call.data
        if pro_type == "PERS":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                  text=f"{word}\n{word_initial}-{person}{number}.{case}.{gender}\n\nГотово!",
                                  reply_markup=None)
        elif (word_initial.lower() in ['сколько', 'кто', 'что', 'несколько', 'нисколько', 'никто','ничто', 'столько', 'некто', 'нечто']) or (pro_type == 'REFL'):
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                  text=f"{word}\n{word_initial}-{case}\n\nГотово!",
                                  reply_markup=None)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                  text=f"{word}\n{word_initial}-{case}.{gender}\n\nГотово!",
                                  reply_markup=None)
        
bot.polling(none_stop=True, interval=0)
