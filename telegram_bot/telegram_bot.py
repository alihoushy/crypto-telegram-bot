# telegram_bot/telegram_bot

import os
import telebot
from database import database
from prettytable import PrettyTable

# Create a new bot object
token = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(token)

# Define start command handler
@bot.message_handler(commands=['start'])
def start_command(message):
    # Define welcome message with emojis
    welcome_message = "👋 Welcome to Bot \n\nYou can use /help command to see the list of available commands."

    # Send welcome message to user
    bot.reply_to(message, welcome_message)

# Define help command handler
@bot.message_handler(commands=['help'])
def help(message):
    response = "Here are the available commands:\n\n"
    response += "/start - Start the bot\n"
    response += "/help - Display available commands\n"
    response += "/signup [email] [password] - signup a new account\n"
    response += "/signin [email] [password] - signin the account\n"
    response += "/about - About the creator\n"
    response += "/run - Run the bot\n"
    bot.reply_to(message, response)

# Define signup command handler
@bot.message_handler(commands=['signup'])
def signup(message):
    try:
        email, password = message.text.split()[1:3]
        resp = database.signup(email=email, password=password)
        if resp:
            bot.reply_to(message, 'SignUp successful!')
    except (IndexError, ValueError):
        bot.reply_to(message, 'Invalid format. Please use /signup [email] [password]')
    except Exception as e:
        bot.reply_to(message, 'Error: {}'.format(str(e)))

# Define signin command handler
@bot.message_handler(commands=['signin'])
def signin(message):
    try:
        email = message.text.split()[1]
        password = message.text.split()[2]
        resp = database.signin(email=email, password=password)
        if resp:
            bot.reply_to(message, 'SignIn successful!')
        else:
            bot.reply_to(message, 'Invalid email or password')
    except:
        bot.reply_to(message, 'Invalid format. Please use /signin [email] [password]')

# Define about command handler
@bot.message_handler(commands=['about'])
def show_ads(message):
    # send the about creator message to the user
    bot.reply_to(message, "Thank's for your attention! We are pro traders :D")

# Define run command handler
@bot.message_handler(commands=['run'])
def help_handler(message):
    # run bot after click on this button
    bot.reply_to(message, "Bot running :D")

    # Before run the bot, user must be authenticated

    # Start trading_bot

# Send pretty table report
def send_report(chat_id, rows=[], data=[]):
    # Create table
    table = PrettyTable()
    table.field_names = rows
    for row in data:
        table.add_row(row)

    # Send table to user
    bot.send_message(chat_id, f"```\n{table.get_string()}\n```", parse_mode="Markdown")

# Init bot
def init():
    # run the bot
    bot.polling()
