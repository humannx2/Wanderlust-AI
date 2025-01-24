from app import db

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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    points = db.Column(db.Integer, default=0)
    badges = db.Column(db.Text, default="")  # Store JSON or comma-separated badges
