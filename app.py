from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import openai
from crewai import Crew
from agents import activity_finder, activity_moderator
from tools import location
from tasks import activity_finder_task, activity_moderator_task

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


@app.route('/')
def home():
    return "Welcome to Wanderlust API!"

if __name__ == '__main__':

    app.run(debug=True)


