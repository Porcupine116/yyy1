from binance.futures import Futures
from pprint import pprint

client = Futures(key='dbefbc809e3e83c283a984c3a1459732ea7db1360ca80c5c2c8867408d28cc83',
                 secret='2b5eb11e18796d12d88f13dc27dbbd02c2cc51ff7059765ed9821957d82bb4d9')

params = {
    'symbol': "BTCUSDT"
}

response = client.mark_price(**params)

pprint(response)