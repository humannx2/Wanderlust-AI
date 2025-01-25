from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import openai
from crewai import Crew
from agents import activity_finder, activity_moderator
from tools import location
from tasks import activity_finder_task, activity_moderator_task
import json

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# # Database configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


crew = Crew(
    agents=[activity_finder, activity_moderator],
    tasks=[activity_finder_task, activity_moderator_task],
    verbose=True,
    memory=True
)

@app.route('/generate_activity',methods={'POSt'})
def generate_activities():
    try:
        data = request.get_json()
        location_input = data.get('location', '')
        category_input = data.get('category', '')
        time_input = data.get('time', '')

        inputs = {
            "location": location_input,
            "category": category_input,
            "time": time_input
        }

        result = crew.kickoff(inputs=inputs)
        output=result.raw

        return jsonify({"result": output})

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/')
def home():
    return "Welcome to Wanderlust API!"

if __name__ == '__main__':

    app.run(debug=True)


