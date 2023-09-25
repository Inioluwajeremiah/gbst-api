from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(15), nullable=False)
    otp = db.Column(db.String(6), nullable=False)
    expiration_time = db.Column(db.DateTime, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

    bloodsugarTest = db.relationship("BloodSugarTest", backref="user")
    childbirthOutcome = db.relationship("ChildBirthOutcome", backref="user")
    clinicalHistory = db.relationship("ClinicalHistory", backref="user")
    diet = db.relationship("Diet", backref="user")
    enrollment = db.relationship("Enrollment", backref="user")
    exercise = db.relationship("Exercise", backref="user")
    FetalKickCount = db.relationship("FetalKickCount", backref="user")
    medicalHistory = db.relationship("MedicalHistory", backref="user")
    obstetricInformation = db.relationship("ObstetricInformation", backref="user")
    predict = db.relationship("Predict", backref="user")
    profile = db.relationship("Profile", backref="user")

class BloodSugarTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id =db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)


class ChildBirthOutcome(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id =db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

class ClinicalHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Integer)
    height = db.Column(db.Integer) 
    bmi = db.Column(db.Integer) 
    armCircumference = db.Column(db.Integer) 
    waistCircumference = db.Column(db.Integer) 
    hipCircumference = db.Column(db.Integer) 
    waistHipCircumference = db.Column(db.Integer) 
    gestationalAge = db.Column(db.Integer) 

    user_id =db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

class Diet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id =db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age_at_last_birthday = db.Column(db.Integer)
    level_of_education =  db.Column(db.String(50))
    marital_status = db.Column(db.String(50))
    religion = db.Column(db.String(50))
    ethnicity = db.Column(db.String(50))
    occupation = db.Column(db.String(200))

    user_id =db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id =db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
class FetalKickCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id =db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

class MedicalHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hypertension = db.Column(db.String(10), nullable=False)
    diabetes = db.Column(db.String(10), nullable=False)
    asthma = db.Column(db.String(10), nullable=False)
    chronicLungDisease  = db.Column(db.String(10), nullable=False)
    sickleCellDisease = db.Column(db.String(10), nullable=False)
    pcos = db.Column(db.String(10), nullable=False)
    diabetesDuration = db.Column(db.Integer, nullable=False)
    gdm = db.Column(db.String(10), nullable=False)
    
    user_id =db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    
class ObstetricInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    noOfPregnancies = db.Column(db.Integer)
    noOfMiscarriages = db.Column(db.Integer)
    noOfVoluntaryPregnacyTermination = db.Column(db.Integer )
    noOfChildbirthDeliveries = db.Column(db.Integer)
    fourKgBirthWeight = db.Column(db.String(10))
    anyStillbirth = db.Column(db.String(10))
    cogenitalMalformation = db.Column(db.String(10))
    lastTimeOFMenstralPeriod = db.Column(db.Integer)
    gestationalAge = db.Column(db.Integer)

    user_id =db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

class Predict(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id =db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id =db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)


