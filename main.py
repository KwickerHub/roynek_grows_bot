import os
import logging
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import requests
import random
import string
from datetime import datetime

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = Flask(__name__)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the bot application
application = Application.builder().token(BOT_TOKEN).build()

async def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

async def the_main(update: Update, context: ContextTypes.DEFAULT_TYPE, command="start"):
    user = update.message.from_user
    user_id = user.id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    referrer_id = context.args[0] if context.args else None

    now = datetime.now()
    formattedDate = now.strftime('%Y-%m-%d')
    formattedTime = now.strftime('%I:%M:%S %p')

    url_plug = "https://roynek.com/alltrenders/codes/Telegram_Bot/Roynek%20Grows%20Bot"
    game_url = f'{url_plug}/pre_game.html'
    calendar_url = "https://docs.google.com/document/d/1lfuj6zKsNyK16RrOSvDD2AmgFedJAaR-2b5xTJwX6iw/edit?usp=sharing"
    telegram_channel_url = "https://t.me/roynek_grows"
    telegram_community = "https://t.me/roynek_grows_coin"

    response = requests.post(f'{url_plug}/check_user.php', data={
        'username': username,
        'tele_id': user_id,
        'referrer_id': referrer_id,
        'first_name': first_name,
        'last_name': last_name
    })
    result = response.json()

    if result["status"]:
        query_params = {
            'hash': result["hash"],
            'tele_id': user_id,
            'username': username,
            'first_name': first_name,
            'last_name': last_name
        }
        game_url_with_params = f"{game_url}?{urlencode(query_params)}"

        keyboard = [
            [InlineKeyboardButton("Play Now", url=game_url_with_params)],
            [InlineKeyboardButton("View Our Calendar", url=calendar_url)],
            [InlineKeyboardButton("Join Our Telegram Channel", url=telegram_channel_url)],
            [InlineKeyboardButton("Join Our Community", url=telegram_community)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        welcome_message = (
            f"🎉 Welcome {username}! 🎉 You are now a Roynekian with Grows Powers \n\n"
            "We're thrilled to have you here. Unlike other Telegram token games, "
            "we are committed and sure of our launch date.\n\n"
            "Click the button below to start playing the game: You can only use this button once. \n\n"
            "To enjoy another session, give the /play command again \n\n"
            "Stay updated with our proposed calendar below.\n\n"
            "Join our Telegram channel for the latest updates and community discussions."
        ) if (command == "start") else (
            "Click the button below to start playing the game: It is a one time button, you can not use it again. \n\n "
            "We have improved the security of telegram games. To enjoy another session, give the /play command again \n\n"
            "Stay updated with our proposed calendar below.\n\n"
            "Join our Telegram channel for the latest updates and community discussions."
        )

        await update.message.reply_text(welcome_message, reply_markup=reply_markup)
    else:
        response = requests.post(f'{url_plug}/register_user.php', data={
            'username': username,
            'tele_id': user_id,
            'referrer_id': referrer_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': None,
            'password': await generate_strong_password(),
            'third_party_id': user_id,
            'signup_date': formattedDate,
            'signup_time': formattedTime,
        })
        result = response.json()

        if result["status"]:
            query_params = {
                'hash': result["hash"],
                'tele_id': user_id,
                'username': username,
                'first_name': first_name,
                'last_name': last_name
            }
            game_url_with_params = f"{game_url}?{urlencode(query_params)}"

            keyboard = [
                [InlineKeyboardButton("Play Now", url=game_url_with_params)],
                [InlineKeyboardButton("View Our Calendar", url=calendar_url)],
                [InlineKeyboardButton("Join Our Telegram Channel", url=telegram_channel_url)],
                [InlineKeyboardButton("Join Our Community", url=telegram_community)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            welcome_message = (
                f"🎉 Welcome {username}! 🎉 You are now a Roynekian with Grows Powers \n\n"
                "We're thrilled to have you here. Unlike other Telegram token games, "
                "we are committed and sure of our launch date.\n\n"
                "Click the button below to start playing the game:\n\n"
                "Stay updated with our proposed calendar by clicking the link below.\n\n"
                "Join our Telegram channel for the latest updates and community discussions."
            ) if (command == "start") else (
                "Click the button below to start playing the game:\n\n"
                "Stay updated with our proposed calendar by clicking the link below.\n\n"
                "Join our Telegram channel for the latest updates and community discussions."
            )

            await update.message.reply_text(welcome_message, reply_markup=reply_markup)
        else:
            await update.message.reply_text('We are having some issues. We are working on fixing it, Hope to see you around.')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await the_main(update=update, context=context, command="start")

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await the_main(update=update, context=context, command="play")

async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    referral_link = f"https://t.me/RoynekGrowsBot?start={user_id}"
    await update.message.reply_text(f'Your referral link is: {referral_link}')

# Add handlers
application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('play', play))
application.add_handler(CommandHandler('referral', referral))

# Set the webhook
application.bot.set_webhook(WEBHOOK_URL)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "ok", 200

if __name__ == '__main__':
    app.run(port=5000)
