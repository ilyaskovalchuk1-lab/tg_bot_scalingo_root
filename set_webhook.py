
import os
import requests

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Переменная TELEGRAM_BOT_TOKEN не установлена!")

APP_NAME = "bottesthohoho"
WEBHOOK_URL = f"https://{APP_NAME}.scalingo.io/webhook/{TOKEN}"

def main():
    print("Удаляем старый вебхук...")
    requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook")

    print("Устанавливаем новый вебхук...")
    resp = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}")
    print("Ответ Telegram:", resp.json())

    print("Проверяем статус...")
    info = requests.get(f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo").json()
    print("Webhook info:", info)

if __name__ == "__main__":
    main()
