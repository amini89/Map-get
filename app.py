from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='.')

# ذخیره موقت نقاط در حافظه
points = []

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')
    if lat is not None and lng is not None:
        points.append({'lat': lat, 'lng': lng})
    return jsonify({"status": "success"})

@app.route('/data')
def get_data():
    return jsonify(points)

@app.route('/')
def sender():
    return send_from_directory('.', 'index.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory('.', 'dashboard.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)