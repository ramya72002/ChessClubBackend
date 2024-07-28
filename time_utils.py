from flask import jsonify
from datetime import datetime

def time_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def serve_time():
    return jsonify({"time": time_now()})
