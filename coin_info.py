from binance.futures import Futures
from threading import Thread
import configure

client = Futures(key=configure.binance_api_key['key'],
                 secret=configure.binance_api_key['secret'])


def get_all(symbol, period):
    global all_info
    params = {
        'symbol': symbol,
        'period': period,
    }

    response = client.long_short_account_ratio(**params)[-1]
    all_info[period]['all'] = {}
    long = round(float(response['longAccount']) * 100)
    short = round(float(response['shortAccount']) * 100)
    all_info[period]['all']['long'] = long
    all_info[period]['all']['short'] = short


def get_top_traders(symbol, period):
    global all_info
    params = {
        'symbol': symbol,
        'period': period,
    }

    all_info[period] = {}
    response = client.top_long_short_position_ratio(**params)[-1]
    all_info[period]['top_traders'] = {}
    long = round(float(response['longAccount']) * 100)
    short = round(float(response['shortAccount']) * 100)
    all_info[period]['top_traders']['long'] = long
    all_info[period]['top_traders']['short'] = short


def get_volumes(symbol, period):
    global all_info
    params = {
        'symbol': symbol,
        'period': period,
    }

    response = client.taker_long_short_ratio(**params)[-1]
    all_info[period]['volumes'] = {}
    buy = round(float(response['buyVol']))
    sell = round(float(response['sellVol']))
    all_info[period]['volumes']['buy'] = buy
    all_info[period]['volumes']['sell'] = sell


def get_price_funding(symbol):
    global all_info
    params = {
        'symbol': symbol
    }
    response = client.mark_price(**params)
    all_info['funding'] = round(float(response['lastFundingRate']) * 100, 4)
    all_info['price'] = round(float(response['estimatedSettlePrice']), 3)


def get_info(symbol):
    global all_info
    periods = ['15m', '1h', '1d']

    threads = []
    all_info = {}
    for period in periods:
        params = {
            'symbol': symbol,
            'period': period,
        }

        t = Thread(target=get_top_traders, args=(symbol, period))
        threads.append(t)

        t = Thread(target=get_all, args=(symbol, period))
        threads.append(t)

        t = Thread(target=get_volumes, args=(symbol, period))
        threads.append(t)

    t = Thread(target=get_price_funding, args=(symbol,))
    threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    return all_info

# from pprint import pprint
# with open('all_coins.txt', encoding='utf-8') as f:
#     data = f.read().split('\n')
#
# for coin in data:
#     print(coin)
#     pprint(get_info(coin + 'USDT'))
#     print('\n\n\n')
