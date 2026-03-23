from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TOKEN = "8603724750:AAGMMiCddbqgx1Hit6VUGm_amfYQE0r4O-8"
CHAT_ID = "6017621623"

# =====================
# SETTINGS
# =====================
SL_PIPS = 5
TP1_PIPS = 5
TP2_PIPS = 10

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })

@app.route("/")
def home():
    return "Bot Running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)

    msg = data.get("message", "")
    
    import re
    numbers = re.findall(r'\d+\.?\d*', msg)

    if not numbers:
        return jsonify({"error": "no price"}), 200

    price = float(numbers[0])

    if "BUY" in msg:
        sl = price - 5
        tp1 = price + 5
        tp2 = price + 10

        text = f"""🟢 XAUUSD BUY

Entry: {price}
SL: {sl}
TP1: {tp1}
TP2: {tp2}

⚡ Sniper Auto"""

    elif "SELL" in msg:
        sl = price + 5
        tp1 = price - 5
        tp2 = price - 10

        text = f"""🔴 XAUUSD SELL

Entry: {price}
SL: {sl}
TP1: {tp1}
TP2: {tp2}

⚡ Sniper Auto"""

    else:
        return jsonify({"error": "no signal"}), 200

    send(text)
    return jsonify({"status": "sent"}), 200