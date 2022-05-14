import telebot
from telebot import types
import configure
import coin_info
import time
import datetime

client = telebot.TeleBot(configure.config['token'])

with open('all_coins.txt', encoding='utf-8') as file:
    all_coins = file.read().split('\n')

zap = {}
ban = set()


@client.message_handler(commands=['start'])
def answer(message):
    markup_inline = types.InlineKeyboardMarkup()
    item_long_short = types.InlineKeyboardButton(text='Топ лонги🟢/шорты🔴', callback_data='longshort')
    item_stat = types.InlineKeyboardButton(text='Данные о монете (лонг/шорт)📊', callback_data='stat')
    item_info = types.InlineKeyboardButton(text='Информация о монете📜', callback_data='info')
    item_trans = types.InlineKeyboardButton(text='Информация о ликвидах и переводах📉📈', callback_data='trans')
    item_calc = types.InlineKeyboardButton(text='Калькулятор усреднения⌨️', callback_data='calc')
    markup_inline.add(item_stat)
    markup_inline.add(item_long_short)
    markup_inline.add(item_calc)
    markup_inline.add(item_info)
    markup_inline.add(item_trans)
    client.send_message(message.chat.id, f"""🫡Шалом Барыга, я бот команды NINJA 🥷🏿
Моя задача, предоставить тебе всю необходимую инфу для профитного трейдинга! 💰
Шо тебя интересует? 🧐""",
                        reply_markup=markup_inline)


@client.callback_query_handler(func=lambda call: True)
def get_user_info(call):
    if call.data == 'stat':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        main_menu = types.KeyboardButton('Главное меню')
        coins = []
        for coin in all_coins:
            item = types.KeyboardButton('/' + coin)
            coins.append(item)

        markup_reply.add(main_menu)
        markup_reply.add(*coins)

        client.send_message(call.message.chat.id, 'Шо барыга, какую монету поторгуем?',
                            reply_markup=markup_reply
                            )
    elif call.data == 'info':
        client.send_message(call.message.chat.id, 'Прости друг, этот раздел в процессе, скоро всё будет'
                            )

    elif call.data == 'calc':
        client.send_message(call.message.chat.id, 'Прости друг, этот раздел в процессе, скоро всё будет'
                            )

    elif call.data == 'trans':
        client.send_message(call.message.chat.id, 'Прости друг, этот раздел в процессе, скоро всё будет'
                            )

    elif call.data == 'longshort':
        client.send_message(call.message.chat.id, 'Прости друг, этот раздел в процессе, скоро всё будет'
                            )


def beauty(value):
    l = []
    t = ''
    value = str(value)[::-1]
    for s in value:
        t += s
        if len(t) >= 3:
            l.append(t)
            t = ''
    if t != '':
        l.append(t)
    return ' '.join(l)[::-1]


@client.message_handler(commands=all_coins)
def get_text(message):
    global zap
    if message.chat.id in ban:
        now = datetime.datetime.now()
        deltatime = now - zap[message.chat.id][-1]
        if deltatime >= datetime.timedelta(minutes=1):
            ban.remove(message.chat.id)
        else:
            d = datetime.timedelta(minutes=1) - deltatime
            client.send_message(message.chat.id, f'Помолчи пока... {d.seconds} sec')
            return
    if message.text.upper()[1:] in all_coins:
        if message.chat.id not in zap:
            zap[message.chat.id] = [datetime.datetime.now()]
        else:
            zap[message.chat.id].append(datetime.datetime.now())
            if len(zap[message.chat.id]) > 3:
                zap[message.chat.id] = zap[message.chat.id][1:]
                deltatime = zap[message.chat.id][-1] - zap[message.chat.id][0]
                ogr = datetime.timedelta(seconds=2)
                if deltatime < ogr:
                    client.send_message(message.chat.id,
                                        'Оох... нарвался ты браток. Отдыхай теперь, нечего тут сообщениями сорить')
                    ban.add(message.chat.id)
                    return

        messagetoedit = client.send_message(message.chat.id, 'Погоди ка братан, найду инфу...')

        try:
            res = coin_info.get_info(message.text.upper()[1:] + 'USDT')

            client.edit_message_text(chat_id=message.chat.id, message_id=messagetoedit.message_id,
                                     text=f"""Короче, смотри шо я тут нарыл на эту монетку:

#{message.text.upper().lstrip("/")} | 💰 {res['price']}$ 
📊 {res['funding']} Фандинг

🕐 Тайм Фрейм: 15м

🐹 Все барыги:
🟩 Лонгуют: {res['15m']['all']['long']}%  🟥 Шортят: {res['15m']['all']['short']}%

💪🏻 Топовые барыги:
🟩 Лонгуют: {res['15m']['top_traders']['long']}%  🟥 Шортят: {res['15m']['top_traders']['short']}% 

☁ Обьемы (лонгов/шортов) {round(res['15m']['volumes']['buy'] / res['15m']['volumes']['sell'], 2)}: 
🟩 Покупки: {beauty(res['15m']['volumes']['buy'])} {message.text.upper().lstrip("/")}
🟥 Продажи: {beauty(res['15m']['volumes']['sell'])} {message.text.upper().lstrip("/")}


🕐 Тайм Фрейм: 1ч

🐹 Все барыги:
🟩 Лонгуют: {res['1h']['all']['long']}%  🟥 Шортят: {res['1h']['all']['short']}% 

💪🏻 Топовые барыги:
🟩 Лонгуют: {res['1h']['top_traders']['long']}%  🟥 Шортят: {res['1h']['top_traders']['short']}% 

☁ Обьемы (лонгов/шортов) {round(res['1h']['volumes']['buy'] / res['1h']['volumes']['sell'], 2)}:
🟩 Покупки: {beauty(res['1h']['volumes']['buy'])} {message.text.upper().lstrip("/")}
🟥 Продажи: {beauty(res['1h']['volumes']['sell'])} {message.text.upper().lstrip("/")}


🕐 Тайм Фрейм: 1д

🐹 Все барыги:
🟩 Лонгуют: {res['1d']['all']['long']}%  🟥 Шортят: {res['1d']['all']['short']}% 

💪🏻 Топовые барыги:
🟩 Лонгуют: {res['1d']['top_traders']['long']}%  🟥 Шортят: {res['1d']['top_traders']['short']}% 

☁ Обьемы (лонгов/шортов) {round(res['1d']['volumes']['buy'] / res['1d']['volumes']['sell'], 2)}: 
🟩 Покупки: {beauty(res['1d']['volumes']['buy'])} {message.text.upper().lstrip("/")}
🟥 Продажи: {beauty(res['1d']['volumes']['sell'])} {message.text.upper().lstrip("/")}

Авторский канал: @ninjacrypto_trade
Чат: @ninjacrypto_chat
Новости: @ninjacrypto_news
Сигналы участников: @ninjacrypto_signal
Самые жирные AirDrop: @ninjacrypto_airdrop
From: @ninja_statbot""")
        except Exception as e:
            client.edit_message_text(chat_id=message.chat.id, message_id=messagetoedit.message_id,
                                     text='Много же вас, барыг. Отдохну немного')
    else:
        client.send_message(message.chat.id, 'Кажется, я не знаю такую монету(')


@client.message_handler(content_types=['text'])
def menu(message):
    if message.text == 'Главное меню':
        markup_inline = types.InlineKeyboardMarkup()
        item_long_short = types.InlineKeyboardButton(text='Топ лонги🟢/шорты🔴', callback_data='longshort')
        item_stat = types.InlineKeyboardButton(text='Данные о монете 📊', callback_data='stat')
        item_info = types.InlineKeyboardButton(text='Информация о монете📜', callback_data='info')
        item_trans = types.InlineKeyboardButton(text='Информация о ликвидах и переводах📉📈', callback_data='trans')
        item_calc = types.InlineKeyboardButton(text='Калькулятор усреднения⌨️', callback_data='calc')
        markup_inline.add(item_stat)
        markup_inline.add(item_long_short)
        markup_inline.add(item_calc)
        markup_inline.add(item_info)
        markup_inline.add(item_trans)
        client.send_message(message.chat.id, f"""🫡Шалом Барыга, я бот команды NINJA 🥷🏿
Моя задача, предоставить тебе всю необходимую инфу для профитного трейдинга! 💰
Шо тебя интересует? 🧐""",
                            reply_markup=markup_inline)


def main():
    while True:
        try:
            client.polling(none_stop=True, interval=0)
        except Exception as e:
            print(e)
            time.sleep(3)


if __name__ == '__main__':
    main()
