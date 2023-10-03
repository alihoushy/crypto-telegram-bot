# trading_bot/trading_bot

from exchange_future.exchange_future import ExchangeFuture
from redis_package.redis_client import redis_client
from redis_package.redis_utils import get_key_value
import asyncio
import json

class TradingBot:
    def __init__(self, symbol, api_key, api_secret, api_passphrase):
        print('TradingBot class __init__')
        self.exchange_future = ExchangeFuture(symbol, api_key, api_secret, api_passphrase)

    async def start(self):
        # Start bot
        print('start()')

        try:
            print('try')

            # Hint: Long(buy) and Short(sell) is a dynamic choise

            # 1. Open first order
            
            # 2. Check for position change event (order created successfully or not)

            # 3. Open other orders (number of orders in this case: 7)
            
            # End.
        except Exception as e:
            print('start close failed with:', str(e))
            # retry or whatever

        return True

    async def check_price_changed(self):
        # Check price change event
        print('check_price_changed()')

        try:
            last_price = None
            while True:
                redis_client.ping()
                value = json.loads(get_key_value('last_price'))
                if value != None:
                    if last_price != None and last_price != value:
                        print('last price is:' + str(value['price']))
                    last_price = value
                await asyncio.sleep(0.01)
        except Exception as e:
            print('check_price_changed close failed with:', str(e))
            # retry or whatever

        return True

    async def check_position_changed(self):
        # Check position change event
        print('check_position_changed()')

        try:
            # doing something
            __variable = None
        except Exception as e:
            print('check_position_changed close failed with:', str(e))
            # retry or whatever

        return True
