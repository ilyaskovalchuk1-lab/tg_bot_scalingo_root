import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("TOKEN")
APP_URL = os.environ.get("APP_URL")

if not TOKEN or not APP_URL:
    raise RuntimeError("Не установлены переменные окружения TOKEN и APP_URL")

TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

# Проверка и установка вебхука
def ensure_webhook():
    resp = requests.get(f"{TELEGRAM_API}/getWebhookInfo").json()
    current = resp.get("result", {}).get("url")
    target = f"{APP_URL}/webhook"

    if current != target:
        print(f"Настраиваю webhook: {target}")
        requests.post(f"{TELEGRAM_API}/setWebhook", data={"url": target})
    else:
        print("Webhook уже настроен")

ensure_webhook()

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        requests.post(f"{TELEGRAM_API}/sendMessage", data={"chat_id": chat_id, "text": f"Ты написал: {text}"})
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
