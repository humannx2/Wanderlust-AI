from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import openai
from crewai import Crew
from agents import activity_finder, activity_moderator, quest_creator, quest_moderator
from tools import location
from tasks import activity_finder_task, activity_moderator_task, quest_creator_task, quest_moderator_task
import json


# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wanderlust.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import models and initialize database
from models import db, User, Activity, Quest, CompletedActivity, CompletedQuest
db.init_app(app)

crew = Crew(
    agents=[activity_finder, activity_moderator],
    tasks=[activity_finder_task, activity_moderator_task],
    verbose=True,
    memory=False
)

crew_quest = Crew(
    agents=[quest_creator,quest_moderator], 
    tasks=[quest_creator_task,quest_moderator_task],
    verbose=True,
    memory=False
)


@app.route('/user/register', methods=['POST'])
def register_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    new_user = User(name=name, email=email, points=0)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id": new_user.id, 
        "name": new_user.name, 
        "points": new_user.points
    }), 201

# User Profile Route
@app.route('/user/profile/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Get completed activities
    completed_activities = CompletedActivity.query.filter_by(user_id=user_id).all()
    activities_details = [{
        'id': ca.activity.id,
        'name': ca.activity.name,
        'category': ca.activity.category,
        'completion_date': ca.completion_date.isoformat()
    } for ca in completed_activities]

    # Get completed quests
    completed_quests = CompletedQuest.query.filter_by(user_id=user_id).all()
    quests_details = [{
        'id': cq.quest.id,
        'title': cq.quest.title,
        'theme': cq.quest.theme,
        'completion_date': cq.completion_date.isoformat()
    } for cq in completed_quests]

    return jsonify({
        "user_id": user.id,
        "name": user.name,
        "points": user.points,
        "completed_activities": activities_details,
        "completed_quests": quests_details,
        "badges": user.badges.split(',') if user.badges else []
    })


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


@app.route('/quest',methods={'POSt'})
def generate_quest():
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

        result = crew_quest.kickoff(inputs=inputs)
        output=result.raw

        return jsonify({"result": output})

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route('/update_completion', methods=['POST'])
def update_completion():
    try:
        data = request.get_json()
        item_type = data.get('type')
        item_id = data.get('id')
        user_id = data.get('user_id')

        if not item_type or not item_id or not user_id:
            return jsonify({"error": "Missing 'type', 'id', or 'user_id' in the request"}), 400

        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        if item_type == 'activity':
            activity = Activity.query.filter_by(id=item_id).first()
            if not activity:
                return jsonify({"error": "Activity not found"}), 404

            completed = CompletedActivity.query.filter_by(user_id=user_id, activity_id=item_id).first()
            if completed:
                return jsonify({"message": "Activity already completed!"}), 400

            new_completion = CompletedActivity(user_id=user_id, activity_id=item_id, completion_date=datetime.utcnow())
            db.session.add(new_completion)

            user.points += 10
            
            # Add badge logic for activities
            if len(CompletedActivity.query.filter_by(user_id=user_id).all()) >= 5:
                if 'Activity Explorer' not in (user.badges or '').split(','):
                    user.badges = (user.badges + ',Activity Explorer' if user.badges else 'Activity Explorer')

            db.session.commit()
            return jsonify({
                "message": f"Activity '{activity.name}' marked as completed!", 
                "points": user.points,
                "badges": user.badges.split(',') if user.badges else []
            }), 200

        elif item_type == 'quest':
            quest = Quest.query.filter_by(id=item_id).first()
            if not quest:
                return jsonify({"error": "Quest not found"}), 404

            completed = CompletedQuest.query.filter_by(user_id=user_id, quest_id=item_id).first()
            if completed:
                return jsonify({"message": "Quest already completed!"}), 400

            new_completion = CompletedQuest(user_id=user_id, quest_id=item_id, completion_date=datetime.utcnow())
            db.session.add(new_completion)

            user.points += 50
            
            # Add badge logic for quests
            if len(CompletedQuest.query.filter_by(user_id=user_id).all()) >= 3:
                if 'Quest Master' not in (user.badges or '').split(','):
                    user.badges = (user.badges + ',Quest Master' if user.badges else 'Quest Master')

            db.session.commit()
            return jsonify({
                "message": f"Quest '{quest.title}' marked as completed!", 
                "points": user.points,
                "badges": user.badges.split(',') if user.badges else []
            }), 200

        else:
            return jsonify({"error": "Invalid 'type'. Must be 'activity' or 'quest'"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/')
def home():
    return "Welcome to Wanderlust API!"

if __name__ == '__main__':

    app.run(debug=True)


