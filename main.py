import logging
from contextlib import asynccontextmanager
from http import HTTPStatus
from telegram import Update
# from telegram.ext import Application, CommandHandler
# from telegram.ext._contexttypes import ContextTypes
from fastapi import FastAPI, Request, Response
from dotenv import load_dotenv
import os

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackGame
from telegram.ext import Application, ApplicationBuilder, CommandHandler, CallbackContext, CallbackQueryHandler
# ContextTypes, Dispatcher
from dotenv import load_dotenv
import requests
from urllib.parse import urlencode
import random
import string
from datetime import datetime
from flask import Flask, request
import asyncio

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Your webhook URL

url_plug = "https://roynek.com/alltrenders/codes/Telegram_Bot/Roynek%20Grows%20Bot"
game_url = f'{url_plug}/pre_game.html'
calendar_url = "https://docs.google.com/document/d/1lfuj6zKsNyK16RrOSvDD2AmgFedJAaR-2b5xTJwX6iw/edit?usp=sharing"
telegram_channel_url = "https://t.me/roynek_grows"
telegram_community = "https://t.me/roynek_grows_coin"
game_short_name = "roynek_grows_game"

# Enhanced logging configuration
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# logger = logging.getLogger(__name__)

now = datetime.now()
formattedDate = now.strftime('%Y-%m-%d')
formattedTime = now.strftime('%I:%M:%S %p')

async def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password


import httpx
from datetime import datetime
from urllib.parse import urlencode

async def the_main(update, context, command="start"):
    if update.callback_query:
        query = update.callback_query
        user = query.from_user
        user_id = user.id
        username = user.username
        first_name = user.first_name
        last_name = user.last_name
        referrer_id = None
    else:
        user = update.message.from_user
        user_id = user.id
        username = user.username
        first_name = user.first_name
        last_name = user.last_name
        # referrer_id = context.args[0] if context.args else None
        referrer_id = None
        # Extract the referral ID from the message text
        if update.message and update.message.text:
            command_parts = update.message.text.split()
            if len(command_parts) > 1:
                referrer_id = command_parts[1]

    async with httpx.AsyncClient() as client:
        response = await client.post(f'{url_plug}/check_user.php', data={
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
            game = CallbackGame()
            keyboard = [
                [InlineKeyboardButton("Play Now", callback_game=game)],
                [InlineKeyboardButton("View Our Calendar", url=calendar_url)],
                [InlineKeyboardButton("Join Our Telegram Channel", url=telegram_channel_url)],
                [InlineKeyboardButton("Join Our Community", url=telegram_community)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.answer(url=game_url_with_params) if (update.callback_query) else await update.message.reply_game(game_short_name=game_short_name, reply_markup=reply_markup)
        else:
            response = await client.post(f'{url_plug}/register_user.php', data={
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
                game = CallbackGame()
                keyboard = [
                    [InlineKeyboardButton("Play Now", callback_game=game)],
                    [InlineKeyboardButton("View Our Calendar", url=calendar_url)],
                    [InlineKeyboardButton("Join Our Telegram Channel", url=telegram_channel_url)],
                    [InlineKeyboardButton("Join Our Community", url=telegram_community)]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_game(game_short_name=game_short_name, reply_markup=reply_markup)
            else:
                await update.message.reply_text('We are having some issues. We are working on fixing it, Hope to see you around.')

async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    username = user.username if user.username else ""
    first_name = user.first_name if user.first_name else ""
    last_name = user.last_name if user.last_name else ""
    d_name = f"{first_name} {last_name}" 
    intro_name = username if username != None else d_name
    welcome_message = (f"🎉 Welcome {intro_name}! 🎉\n"
    "You are now a Roynekian with Grows Powers\n\n"
    "🚀 We're thrilled to have you here. Unlike other Telegram token games, "
    "we are committed and sure of our launch date.\n\n"
    "👉 Click the button below to start playing the game: \n\n"
    "🔒 We have improved the security of Telegram Games. \n\n"
    "📅 Stay updated with our proposed calendar below.\n\n"
    "💬 Join our Telegram channel for the latest updates and community discussions.")
    
    await update.message.reply_text(welcome_message)
    await the_main(update=update, context=context, command="start")

async def play(update: Update, context: CallbackContext):
    await the_main(update=update, context=context, command="play")

async def referral(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_id = user.id
    referral_link = f"https://t.me/RoynekGrowsBot?start={user_id}"
    await update.message.reply_text(f'Your referral link is: {referral_link}')


async def present_game(update: Update, context: CallbackContext):
    #add game_short_name value (despite the doc saying theres no  need to add it)
    # game.game_short_name=game_short_name

    #Create the actual button
    # buttons = [[InlineKeyboardButton(text="Show Menu", url=game_url ,callback_game=game)]] 
    game = CallbackGame() 
    buttons = [[InlineKeyboardButton(text="Play",callback_game=game)]] 

    #Send game with custom inline button
    keyboard_markup = InlineKeyboardMarkup(buttons)
    await context.bot.send_game(chat_id=update.effective_chat.id,game_short_name=game_short_name,reply_markup=keyboard_markup) 

async def handle_callback_query(update: Update, context: CallbackContext):
    await the_main(update=update, context=context, command="play")
    # query = update.callback_query
    # user = query.from_user

    # user_details = {
    #     "id": user.id,
    #     "first_name": user.first_name,
    #     "last_name": user.last_name,
    #     "username": user.username,
    #     "language_code": user.language_code
    # }

    # game_short_name_rec = query.game_short_name

    # print("User Details:", user_details)

    # Answer the callback query with the game URL
    # await query.answer(url=game_url)
    # query = update.callback_query
    # print(query)
    # # Answer the callback query with the game URL
    # await query.answer(url=game_url)


# async def handler(update, context):
#     # Telegram understands UTF-8, so encode text for unicode compatibility
#     text = str(update.message.text.encode('utf-8').decode() )
#     print("got text message :", text)
#     if ("//start" in text and len(text) <= 10):
#         print("went here 1") 
#         #await start(update, context)
#     elif("//play" in text and len(text) <= 10): 
#         await play(update, context)
#         print("went here 2") 
#     elif("//referral" in text and len(text) <= 10): 
#         await referral(update, context)
#         print("went here 3")
#     else:
#         print("went here 4")  

async def handle_text(update: Update):
    text = update.message.text.strip()
    if text.startswith("/start"):
        await start(update, application)
    elif text.startswith("/play"):
        await play(update, application)
    elif text.startswith("/referral"):
        await referral(update, application)
    elif update.callback_query:
        await handle_callback_query(update, application)
    else:
        print("some text passed in...")
        pass



# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Your webhook URL

# Initialize python telegram bot
application = (
    Application.builder()
    .token(BOT_TOKEN)
    .build()
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await application.bot.setWebhook(f"{WEBHOOK_URL}/webhook")
    async with application:
        await application.start()
        yield
        await application.stop()

# Initialize FastAPI app
app = FastAPI(lifespan=lifespan)

@app.post("/webhook")
async def process_update(request: Request):
    req = await request.json()
    logger.info(f"Received update: {req}")
    update = Update.de_json(req, application.bot)
    logger.info(f"Processing update: {update}")
    if update.message:
        await handle_text(update)
    await application.process_update(update)

    return Response(status_code=HTTPStatus.OK)

# async def start(update: Update, context: CallbackContext ):
#     """Send a message when the command /start is issued."""
#     print("atleaste we came here....")
#     logger.info(f"Start command received from user: {update.message.from_user.id}")
#     await update.message.reply_text("starting...")


# Add the command handler to the application
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(handle_callback_query))
# Run the application with Uvicorn
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
