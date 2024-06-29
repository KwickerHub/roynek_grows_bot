import requests
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()
# BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Your webhook URL
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# WEBHOOK_URL = 'https://your-app-url/webhook'
# WEBHOOK_URL = "http://0.0.0.0:8000"

url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook'
data = {'url': WEBHOOK_URL}

response = requests.post(url, data=data)
print(response.json())
