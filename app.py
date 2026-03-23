from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = "8603724750:AAGMMiCddbqgx1Hit6VUGm_amfYQE0r4O-8"
CHAT_ID = "6017621623"

@app.route('/')
def home():
    return "Bot is running"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    msg = data.get("message", "🔥 Signal received")

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })

    return "ok"

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)