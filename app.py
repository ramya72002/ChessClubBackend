from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 1

app = Flask(__name__)
CORS(app)
load_dotenv()

# Get the MongoDB URI from the environment variable
mongo_uri = os.getenv('MONGO_URI')
# MongoDB setup
client = MongoClient(mongo_uri)
db = client.chessclub
users_collection = db.users

@app.route('/')
def home():
    return "Hello, Flask on Vercel!"

def time_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

@app.route('/signup', methods=['POST'])
def signup():
    user_data = request.get_json()
    if user_data:
        parent_first_name = user_data.get('parentFirstName')
        parent_last_name = user_data.get('parentLastName')
        kid_first_name = user_data.get('kidFirstName')
        kid_last_name = user_data.get('kidLastName')
        email = user_data.get('email')
        phone_number = user_data.get('phone')

        # Check if user already exists
        existing_user = users_collection.find_one({
            'email': email,
            'phone': phone_number
        })
        if existing_user:
            return jsonify({'error': 'User already exists. Please login.'}), 400

        # Add new user data
        new_user = {
            'parentFirstName': parent_first_name,
            'parentLastName': parent_last_name,
            'kidFirstName': kid_first_name,
            'kidLastName': kid_last_name,
            'email': email,
            'phone': phone_number,
            'createdAt': time_now()
        }
        users_collection.insert_one(new_user)
        return jsonify({'success': True}), 201
    else:
        return jsonify({'error': 'Invalid data format.'}), 400


@app.route('/signin', methods=['POST'])
def signin():
    user_data = request.get_json()
    if not user_data or 'email' not in user_data:
        return jsonify({'error': 'Email is required.'}), 400
    
    email = user_data.get('email')
    
    # Check if user exists
    existing_user = users_collection.find_one({'email': email})
    if existing_user:
        return jsonify({'success': True, 'message': 'Sign in successful.'}), 200
    else:
        return jsonify({'error': 'Email not registered. Please sign up.'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)