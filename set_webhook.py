
import os
import requests

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Переменная TELEGRAM_BOT_TOKEN не установлена!")

# Prefer explicit BASE_URL (e.g., https://myapp.scalingo.io) if provided
BASE_URL = os.getenv("BASE_URL")
if not BASE_URL:
    # Fallback to APP_NAME if provided (legacy)
    APP_NAME = os.getenv("APP_NAME")
    if not APP_NAME:
        raise RuntimeError("Нужно задать BASE_URL или APP_NAME для формирования URL вебхука")
    BASE_URL = f"https://{APP_NAME}.scalingo.io"

WEBHOOK_URL = f"{BASE_URL}/webhook/{TOKEN}"

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
