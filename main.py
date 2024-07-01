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


# async def the_main(update: Update, context: CallbackContext, command="start"):
#     if update.callback_query:
#         #await handle_callback_query(update, context)
#         query = update.callback_query
#         user = query.from_user
#         user_id = user.id
#         username = user.username
#         first_name = user.first_name
#         last_name = user.last_name
#         referrer_id = None

#         # game_short_name_rec = query.game_short_name
#         # print("User Details:", user_details)
#     else:
#         # Handle other types of updates, like messages, etc.
#         # pass
#         user = update.message.from_user
#         user_id = user.id
#         username = user.username
#         first_name = user.first_name
#         last_name = user.last_name
#         referrer_id = context.args[0] if context.args else None

  
#     response = requests.post(f'{url_plug}/check_user.php', data={
#         'username': username,
#         'tele_id': user_id,
#         'referrer_id': referrer_id,
#         'first_name': first_name,
#         'last_name': last_name
#     })
#     result = response.json()

#     if result["status"]:
#         query_params = {
#             'hash': result["hash"],
#             'tele_id': user_id,
#             'username': username,
#             'first_name': first_name,
#             'last_name': last_name
#         }
#         game_url_with_params = f"{game_url}?{urlencode(query_params)}"
#         game = CallbackGame() 
#         # buttons = [[InlineKeyboardButton(text="Show Menu",callback_game=game)]] 
        
#         keyboard = [
#             # [InlineKeyboardButton("Play Now", url=game_url_with_params)],
#             [InlineKeyboardButton("Play Now",callback_game=game)],
#             [InlineKeyboardButton("View Our Calendar", url=calendar_url)],
#             [InlineKeyboardButton("Join Our Telegram Channel", url=telegram_channel_url)],
#             [InlineKeyboardButton("Join Our Community", url=telegram_community)]
#         ]
#         reply_markup = InlineKeyboardMarkup(keyboard)

#         # welcome_message = (
#         #     f"🎉 Welcome {username}! 🎉 You are now a Roynekian with Grows Powers \n\n"
#         #     "We're thrilled to have you here. Unlike other Telegram token games, "
#         #     "we are committed and sure of our launch date.\n\n"
#         #     "Click the button below to start playing the game: You can only use this button once. \n\n"
#         #     "To enjoy another session, give the /play command again \n\n"
#         #     "Stay updated with our proposed calendar below.\n\n"
#         #     "Join our Telegram channel for the latest updates and community discussions."
#         # ) if (command == "start") else (
#         #     "Click the button below to start playing the game: It is a one time button, you can not use it again. \n\n "
#         #     "We have improved the security of telegram games. To enjoy another session, give the /play command again \n\n"
#         #     "Stay updated with our proposed calendar below.\n\n"
#         #     "Join our Telegram channel for the latest updates and community discussions."
#         # )

#         # await update.message.reply_text(welcome_message, reply_markup=reply_markup)
#         # await update.message.reply_game(game_short_name=game_short_name,reply_markup=reply_markup)
#         await query.answer(url=game_url_with_params) if (update.callback_query) else await update.message.reply_game(game_short_name=game_short_name,reply_markup=reply_markup)
#         # await context.bot.send_game(chat_id=update.effective_chat.id,game_short_name=game_short_name,reply_markup=reply_markup) 
#     else:
#         response = requests.post(f'{url_plug}/register_user.php', data={
#             'username': username,
#             'tele_id': user_id,
#             'referrer_id': referrer_id,
#             'first_name': first_name,
#             'last_name': last_name,
#             'email': None,
#             'password': await generate_strong_password(),
#             'third_party_id': user_id,
#             'signup_date': formattedDate,
#             'signup_time': formattedTime,
#         })
#         result = response.json()

#         if result["status"]:
#             query_params = {
#                 'hash': result["hash"],
#                 'tele_id': user_id,
#                 'username': username,
#                 'first_name': first_name,
#                 'last_name': last_name
#             }
#             game_url_with_params = f"{game_url}?{urlencode(query_params)}"
#             game = CallbackGame() 
#             # buttons = [[InlineKeyboardButton(text="Show Menu",callback_game=game)]] 

#             keyboard = [
#                 # [InlineKeyboardButton("Play Now", url=game_url_with_params)],
#                 [InlineKeyboardButton(text="Play Now",callback_game=game)],
#                 [InlineKeyboardButton("View Our Calendar", url=calendar_url)],
#                 [InlineKeyboardButton("Join Our Telegram Channel", url=telegram_channel_url)],
#                 [InlineKeyboardButton("Join Our Community", url=telegram_community)]
#             ]
#             reply_markup = InlineKeyboardMarkup(keyboard)

#             # welcome_message = (
#             #     f"🎉 Welcome {username}! 🎉 You are now a Roynekian with Grows Powers \n\n"
#             #     "We're thrilled to have you here. Unlike other Telegram token games, "
#             #     "we are committed and sure of our launch date.\n\n"
#             #     "Click the button below to start playing the game:\n\n"
#             #     "Stay updated with our proposed calendar below.\n\n"
#             #     "Join our Telegram channel for the latest updates and community discussions."
#             # ) if (command == "start") else (
#             #     "Click the button below to start playing the game:\n\n"
#             #     "Stay updated with our proposed calendar below.\n\n"
#             #     "Join our Telegram channel for the latest updates and community discussions."
#             # )

#             # Send the welcome message with inline buttons
#             # await update.message.reply_text(welcome_message, reply_markup=reply_markup)
#             # Send the game message
#             # await context.bot.send_game(chat_id=update.effective_chat.id, game_short_name=game_short_name)
#             # await context.bot.send_game(chat_id=update.effective_chat.id, game_short_name=game_short_name)

#             # update.message.reply_text(welcome_message)
#             await update.message.reply_game(game_short_name=game_short_name, reply_markup=reply_markup)
#             # await context.bot.send_game(chat_id=update.effective_chat.id, game_short_name=game_short_name, reply_markup=reply_markup) 
#         else:
#             await update.message.reply_text('We are having some issues. We are working on fixing it, Hope to see you around.')

async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    username = user.username
    welcome_message = (f"🎉 Welcome {username}! 🎉 You are now a Roynekian with Grows Powers \n\n"
    "We're thrilled to have you here. Unlike other Telegram token games, "
    "we are committed and sure of our launch date.\n\n"
    "Click the button below to start playing the game: You can only use this button once. \n\n"
    "To enjoy another session, give the /play command again \n\n"
    "Stay updated with our proposed calendar below.\n\n"
    "Join our Telegram channel for the latest updates and community discussions.")
    
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


async def handler(update, context):
    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = str(update.message.text.encode('utf-8').decode() )
    print("got text message :", text)
    if (text.startswith("/start")): await start(update, context)
    elif(text.startswith("/play")): await play(update, context)
    elif(text.startswith("/referral")): await referral(update, context)
    
    # text = update.message.text.encode('utf-8').decode()
    # print("got text message :", text)

    # chat_id = update.message.chat.id
    # msg_id = update.message.message_id
    # response = "hello made..."
    # # await application.bot.send_message(chat_id=chat_id, text=response, reply_to_message_id=msg_id) 
    # await referral(update, context)

app = Flask(__name__)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# # Initialize the bot application
application = Application.builder().token(BOT_TOKEN).build()


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        # print(data["message"]["text"])
        message = data.get('message', '')  # Ensure you correctly extract the 'text' field
        print("Received text:", message)  # Check the extracted text

        update = Update.de_json(data, application.bot)
        # print(update)
        # # get the chat_id to be able to respond to the same user
        chat_id = update.message.chat.id
        # # get the message id to be able to reply to this specific message
        msg_id = update.message.message_id

        # # Telegram understands UTF-8, so encode text for unicode compatibility
        text = update.message.text
        # print(f"got text message : {text}: {update.message.chat.first_name}: {update.message.chat.username} ")

        # Handle the update through the application
        # asyncio.run(application.process_update(update) )

        # here we call our super AI
        # response = get_response(text)
        response = "hello made..."

        # now just send the message back
        # notice how we specify the chat and the msg we reply to
        # asyncio.run(application.bot.send_message(chat_id=chat_id, text=response, reply_to_message_id=msg_id) )
        # bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)

        asyncio.run( handler(update, application) )

        return 'ok'
    
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")


if __name__ == '__main__':
    # app.run(debug=True, port=8000)
    app.run(port=8000)

