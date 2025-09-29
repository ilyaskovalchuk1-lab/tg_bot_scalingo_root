
import os
import requests
from flask import Flask, request

app = Flask(__name__)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Environment variable TELEGRAM_BOT_TOKEN is not set")

@app.route("/")
def index():
    return "Bot is running!"

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json(silent=True) or {}
    message = update.get("message") or update.get("edited_message") or {}
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    text = message.get("text")

    # Ignore updates without text messages (callbacks, joins, etc.)
    if not (chat_id and text):
        return "ignored", 200

    try:
        send_message(chat_id, f"Echo: {text}")
    except Exception:
        # Do not fail webhook; log in server logs
        app.logger.exception("Failed to send message")

    return "ok", 200

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
