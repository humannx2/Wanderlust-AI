from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import openai

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# OpenAI API key (replace with your actual key)
openai.api_key = "your-openai-api-key"

# Import models
class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(10), nullable=False)

class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    steps = db.Column(db.Text, nullable=False)  # Store steps as JSON or comma-separated

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Integer, default=0)

@app.route('/')
def home():
    return "Welcome to Wanderlust API!"

if __name__ == '__main__':

    app.run(debug=True)
