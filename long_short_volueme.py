from binance.futures import Futures
from pprint import pprint

client = Futures(key='dbefbc809e3e83c283a984c3a1459732ea7db1360ca80c5c2c8867408d28cc83',
                 secret='2b5eb11e18796d12d88f13dc27dbbd02c2cc51ff7059765ed9821957d82bb4d9')

params = {
    'symbol': "BTCUSDT",
    'period': "15m"
}

response1 = client.top_long_short_position_ratio(**params)
response2 = client.long_short_account_ratio(**params)
response3 = client.taker_long_short_ratio(**params)

#pprint(response1)
#pprint(response2)
pprint(response3)