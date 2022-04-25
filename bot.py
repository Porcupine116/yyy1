import telebot
import configure
import long_short_volueme
import price_fubding
from telebot import types


client = telebot.TeleBot(configure.config['token'])

@client.message_handler(commands = ['start'])
def get_user_info(message):
    markup_inline = types.InlineKeyboardMarkup()
    item_statistics = types.InlineKeyboardButton(text = 'Статистика монет', callback_data = 'statistics')
    item_longshort = types.InlineKeyboardButton(text='Статистика лонгов и шортов', callback_data ='longshort')

    markup_inline.add(item_statistics, item_longshort)
    client.send_message(message.chat.id, 'Шалом Барыга, что хотелось бы посмотреть?)',
                        reply_markup = markup_inline
    )

@client.callback_query_handler(func = lambda call:True)
def answer(call):
    if call.data == 'statistics':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item_btc = types.KeyboardButton('BTC')
        item_eth = types.KeyboardButton('ETH')

        markup_reply.add(item_eth, item_btc)
        client.send_message(call.message.chat.id, 'Шо барыга, какую монету поторгуем?',
                            reply_markup = markup_reply
                            )

    elif call.data == 'longshort':
        client.send_message(call.message.chat.id, 'В скором времени и это у нас будет')

@client.message_handler(content_types=['text'])
def get_text(message):
    if message.text == 'BTC':
        client.send_message(message.chat.id, """#BTC | 🇺🇸 44 116,32 $ |
🔴 -0.0019 Funding
👮🏻 BTC.D 42.05%



🕐 Time frame: 15m

🐹 ALL:
🟩 Long:  🟥 Short: 

💪🏻 Top Traders:
🟩 Long:  🟥 Short: 

☁ Volumes (long/short): 
🟩 Buy:  BTC
🟥 Sell: 


🕐 Time frame: 1h

🐹 ALL:
🟩 Long:  🟥 Short: 

💪🏻 Top Traders:
🟩 Long: 53% 🟥 Short: 47%

☁ Volumes (long/short): 1.3
🟩 Buy: 2 979 BTC
🟥 Sell: 2 300 BTC


🕐 Time frame: 1d

🐹 ALL:
🟩 Long: 52% 🟥 Short: 48%

💪🏻 Top Traders:
🟩 Long: 53% 🟥 Short: 47%

☁ Volumes (long/short): 0.95
🟩 Buy: 34 027 BTC
🟥 Sell: 35 993 BTC


Авторский канал: @ninjacrypto_trade
Чат: @ninjacrypto_chat
Новости: @ninjacrypto_news
Сигналы участников: @ninjacrypto_signal
Самые жирные AirDrop: @ninjacrypto_airdrop
From: @ninjacrypto1bot""")
    elif message.text == 'ETH':
        client.send_message(message.chat.id, 'ты дядя не наглей, торгую только биток')


client.polling(none_stop = True, interval = 0)
