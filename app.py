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
    signal = data.get("message", "").upper()

    price = float(data.get("price", 0))

    if price == 0:
        return jsonify({"error": "No price"}), 400

    if "BUY" in signal:
        sl = price - SL_PIPS
        tp1 = price + TP1_PIPS
        tp2 = price + TP2_PIPS

        msg = f"""🟢 XAUUSD BUY

Entry: {price}
SL: {sl}
TP1: {tp1}
TP2: {tp2}

⚡ Sniper Auto"""

        send(msg)

    elif "SELL" in signal:
        sl = price + SL_PIPS
        tp1 = price - TP1_PIPS
        tp2 = price - TP2_PIPS

        msg = f"""🔴 XAUUSD SELL

Entry: {price}
SL: {sl}
TP1: {tp1}
TP2: {tp2}

⚡ Sniper Auto"""

        send(msg)

    return jsonify({"status": "ok"}), 200

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)