
import requests

bot_token = 'your_telegram_bot_token'
response = requests.get(f'https://api.telegram.org/bot{bot_token}/getWebhookInfo')
print(response.json())
