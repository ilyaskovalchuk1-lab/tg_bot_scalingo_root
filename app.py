
import os
import requests
from flask import Flask, request

app = Flask(__name__)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

@app.route("/")
def index():
    return "Bot is running!"

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    if not update:
        return "No update", 400

    chat_id = update.get("message", {}).get("chat", {}).get("id")
    text = update.get("message", {}).get("text")

    if chat_id and text:
        send_message(chat_id, f"Echo: {text}")

    return "ok", 200

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
