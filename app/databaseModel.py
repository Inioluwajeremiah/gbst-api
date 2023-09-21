from app import db
from flask_login import UserMixin

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(15), nullable=False)
    otp = db.Column(db.String(6), nullable=False)
    expiration_time = db.Column(db.DateTime, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)



