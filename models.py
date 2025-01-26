from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    points = db.Column(db.Integer, default=0)
    badges = db.Column(db.Text, default="")

    # Relationships
    completed_activities = db.relationship('CompletedActivity', back_populates='user', cascade='all, delete-orphan')
    completed_quests = db.relationship('CompletedQuest', back_populates='user', cascade='all, delete-orphan')

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(10), nullable=False)
    time_estimate = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(120), nullable=False)

class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    steps = db.Column(db.Text, nullable=False)  # Store JSON or comma-separated activities
    theme = db.Column(db.String(120), nullable=False)
    difficulty = db.Column(db.String(10), nullable=False)

class CompletedActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    completion_date = db.Column(db.DateTime, nullable=False)  # To track when the activity was completed

    # Relationships
    user = db.relationship('User', back_populates='completed_activities')
    activity = db.relationship('Activity')

class CompletedQuest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quest_id = db.Column(db.Integer, db.ForeignKey('quest.id'), nullable=False)
    completion_date = db.Column(db.DateTime, nullable=False)  # To track when the quest was completed

    # Relationships
    user = db.relationship('User', back_populates='completed_quests')
    quest = db.relationship('Quest')