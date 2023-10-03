# exchange_future/exchange_future

import ccxt.async_support as ccxt
import sys
import asyncio

print('CCXT Version:', ccxt.__version__)

class ExchangeFuture:
    def __init__(self, symbol, api_key, api_secret, api_passphrase):
        print('ExchangeFuture class __init__')
        self.symbol = symbol
        self.leverage = 5
        self.wait_time = 5
        self.paper_trading = True
        self.order_sizes = { self.symbol: 0.001 }
        self.exchange = ccxt.kucoinfutures({ 'apiKey': api_key, 'secret': api_secret, 'password': api_passphrase })

    async def buy(self, amount, price, size):
        # Place a buy order for `amount` at market
        print('buy()')
        try:
            response = await self.exchange.create_market_order(symbol=self.symbol, side='buy', amount=amount, price=price, leverage=self.leverage, size=size)
            return response
        except Exception as e:
            print(self.exchange.id, 'create_market_order(buy) failed with:', str(e))
            # retry or whatever

    async def sell(self, amount, price, size):
        # Place a sell order for `amount` at market
        print('sell()')
        try:
            response = await self.exchange.create_market_order(symbol=self.symbol, side='sell', amount=amount, price=price, leverage=self.leverage, size=size)
            return response
        except Exception as e:
            print(self.exchange.id, 'create_market_order(sell) failed with:', str(e))
            # retry or whatever            

    async def fetch_balance(self):
        # Get the current balance for the account associated with `api_key`
        print('fetch_balance()')
        try:
            balance = await self.exchange.fetch_balance()
            print(balance)
            await asyncio.sleep(0.01)
            return
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(self.exchange.id, 'fetch_currencies failed with:', str(e))
            # retry or whatever
        finally:
            await self.exchange.close()

    async def fetch_currencies(self):
        # Get the last price of symbol from tickers
        print('fetch_currencies()')
        try:
            currencies = await self.exchange.fetch_currencies()
            print(currencies)
            await asyncio.sleep(0.01)
            return
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(self.exchange.id, 'fetch_currencies failed with:', str(e))
            # retry or whatever
        finally:
            await self.exchange.close()

    async def check_requirements(self):
        # Check requirements before running bot
        print('check_requirements()')
        try:
            if not self.exchange.has['fetchOrder'] or not self.exchange.has['fetchOpenOrders'] or not self.exchange.has['fetchOrderBook']:
                print(self.exchange.id, "does not support fetchOrder, fetchOpenOrders or fetchOrderBook")
                sys.exit()

            if not self.exchange.has['fetchMarkets']:
                print(self.exchange.id, "does not support fetchMarkets")
                sys.exit()

            if not self.exchange.has['fetchPositions']:
                print(self.exchange.id, "does not support fetchPositions")
                sys.exit()
        except Exception as e:
            print(self.exchange.id, 'close failed with:', str(e))
            # retry or whatever

    async def close(self):
        # Close session of ccxt client
        print('close()')
        try:
            await self.exchange.close()
        except Exception as e:
            print(self.exchange.id, 'close failed with:', str(e))
            # retry or whatever
