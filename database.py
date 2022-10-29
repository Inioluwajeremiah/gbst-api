from datetime import datetime
from flask_sqlalchemy import SQLALchemy

db = SQLALchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_updated = db.Column(db.DateTime, onupdate=datetime.now())
    dietIntervention = db.relationship('DietIntervention', backref="user")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return 'User>>> {self.username}'


class DietIntervention(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diet_image_url = db.Column(db.Text, nullable=False)
    diet_title = db.Column(db.String(150), nullable=False)
    diet_description = db.Column(db.Text(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reads = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)

    def __repr__(self) -> str:
        return 'User>>> {self.diet_title}'
