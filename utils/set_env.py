import argparse, os

# Define command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--sandbox', action='store_true', help='Use sandbox account')
args = parser.parse_args()

# Set environment variables based on command-line argument
def setEnv():
    sandbox_prefix = 'SANDBOX_' if args.sandbox else ''
    return {
        'exchange_symbol': os.getenv(sandbox_prefix + 'EXCHANGE_SYMBOL'),
        'future_api_key': os.getenv(sandbox_prefix + 'FUTURE_API_KEY'),
        'future_api_secret': os.getenv(sandbox_prefix + 'FUTURE_API_SECRET'),
        'future_api_passphrase': os.getenv(sandbox_prefix + 'FUTURE_API_PASSPHRASE'),
        'account_trading_password': os.getenv(sandbox_prefix + 'ACCOUNT_TRADING_PASSWORD')
    }
