import os, asyncio, logging
from dotenv import load_dotenv
from exchange_future_socket.exchange_future_socket import ExchangeFutureSocket
from trading_bot.trading_bot import TradingBot
import asyncio
import threading
from utils.print_animation import print_animation2
from utils.set_env import setEnv
from telegram_bot import telegram_bot

# Load environment variables from .env file
load_dotenv()

# Print animation
print_animation2()

# Enable socks proxy for local development
proxy = os.getenv('SOCKS5_PROXY_URL')
os.environ['socks_proxy'] = proxy
os.environ['SOCKS_PROXY'] = proxy
os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Set env
envs = setEnv()

# Run telegram bot
telegram_bot.init()

# Create objects
exchange_future_socket = ExchangeFutureSocket(envs['exchange_symbol'], envs['future_api_key'], envs['future_api_secret'], envs['future_api_passphrase'])
trading_bot = TradingBot(envs['exchange_symbol'], envs['future_api_key'], envs['future_api_secret'], envs['future_api_passphrase'])

# Create the coroutines for REST and WebSocket connections
rest_coroutines = [
    trading_bot.check_price_changed(),
    # trading_bot.check_position_changed(),
]
ws_coroutines = [
    exchange_future_socket.get_realtime_symbol_ticker(),
    # exchange_future_socket.position_change_events(),
]

# Define a function to run the coroutines in separate threads
def run_in_thread(coro_list):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.gather(*coro_list))

# Create threads to run the coroutines
rest_thread = threading.Thread(target=run_in_thread, args=(rest_coroutines,))
ws_thread = threading.Thread(target=run_in_thread, args=(ws_coroutines,))

# Start the threads
rest_thread.start()
ws_thread.start()

# Wait for the threads to finish
rest_thread.join()
ws_thread.join()
