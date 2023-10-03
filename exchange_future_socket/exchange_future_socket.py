# exchange_future_socket/exchange_future_socket

from kucoin_futures.client import WsToken
from kucoin_futures.ws_client import KucoinFuturesWsClient
from redis_package.redis_client import redis_client
from redis_package.redis_utils import set_key_value
import asyncio
import json

class ExchangeFutureSocket:
     def __init__(self, symbol, api_key, api_secret, api_passphrase):
          print('ExchangeFutureSocket class __init__')
          self.symbol = symbol
          self.api_key = api_key
          self.api_secret = api_secret
          self.api_passphrase = api_passphrase
          self.public_channel_info = {}
          self.private_channel_info = {}

     def get_public_channel_info(self):
          # Public Channels
          try:
               client = WsToken()
               self.private_channel_info = client.get_ws_token(is_private=False)
               return client
          except Exception as e:
               print('get_public_channel_info close failed with:', str(e))
               # retry or whatever

     def get_private_channel_info(self):
          # Private Channels
          try:
               client = WsToken(key=self.api_key, secret=self.api_secret, passphrase=self.api_passphrase, is_sandbox=False)
               self.public_channel_info = client.get_ws_token(is_private=True)
               return client
          except Exception as e:
               print('get_private_channel_info close failed with:', str(e))
               # retry or whatever

     async def get_realtime_symbol_ticker(self):
          # Get Real-Time Symbol Ticker Socket
          print('get_realtime_symbol_ticker()')
          try:
               client = self.get_public_channel_info()
               ws_client = await KucoinFuturesWsClient.create(None, client, self.deal_msg, private=False)
               await ws_client.subscribe('/contractMarket/execution:' + self.symbol)
               while True:
                    await asyncio.sleep(0.01)
          except Exception as e:
               print('get_realtime_symbol_ticker close failed with:', str(e))
               # retry or whatever

     async def position_change_events(self):
          # Get Position Change Events
          print('position_change_events()')
          try:
               client = self.get_private_channel_info()
               ws_client = await KucoinFuturesWsClient.create(None, client, self.deal_msg, private=True)
               await ws_client.subscribe('/contract/position:' + self.symbol)
               while True:
                    await asyncio.sleep(0.01)
          except Exception as e:
               print('position_change_events close failed with:', str(e))
               # retry or whatever

     async def deal_msg(self, msg):
          # Deal Socket Messages
          if '/contractMarket/execution:' in msg['topic']:
               # Redis
               redis_client.ping()
               data = { "topic": msg['topic'], "price": msg['data']['price'] }
               set_key_value("last_price", json.dumps(data))
