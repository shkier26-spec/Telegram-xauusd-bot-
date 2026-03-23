from flask import Flask, request, jsonify
import requests
import os
import re

app = Flask(__name__)

# =====================
# 🔑 SETTINGS
# =====================
TOKEN = "8603724750:AAGMMiCddbqgx1Hit6VUGm_amfYQE0r4O-8"
CHAT_ID = "6017621623"

SL_PIPS = 5
TP1_PIPS = 5
TP2_PIPS = 10

# =====================
# 📩 SEND TO TELEGRAM
# =====================
def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": msg
        })
    except Exception as e:
        print("Error sending:", e)

# =====================
# 🏠 HOME
# =====================
@app.route("/")
def home():
    return "Bot Running"

# =====================
# 🚀 WEBHOOK
# =====================
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)

        msg = data.get("message", "")

        # استخراج السعر من النص
        numbers = re.findall(r'\d+\.?\d*', msg)
        price = float(numbers[0]) if numbers else 0

        if "BUY" in msg:
            sl = price - SL_PIPS
            tp1 = price + TP1_PIPS
            tp2 = price + TP2_PIPS

            text = f"""🟢 XAUUSD BUY

Entry: {price}
SL: {sl}
TP1: {tp1}
TP2: {tp2}

⚡ Sniper Auto"""

            send(text)

        elif "SELL" in msg:
            sl = price + SL_PIPS
            tp1 = price - TP1_PIPS
            tp2 = price - TP2_PIPS

            text = f"""🔴 XAUUSD SELL

Entry: {price}
SL: {sl}
TP1: {tp1}
TP2: {tp2}

⚡ Sniper Auto"""

            send(text)

        else:
            send("⚠️ Unknown signal received")

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        send(f"❌ ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500

# =====================
# ▶️ RUN
# =====================
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)