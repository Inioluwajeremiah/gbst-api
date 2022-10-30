from flask import Flask, request, jsonify
import pickle
import pandas as pd
from werkzeug.security import check_password_hash, generate_password_hash
import validators
# from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
# from . database import User, db
from datetime import datetime
import os

from status_codes import HTTP_200_OK, HTTP_201_CREATED
from status_codes import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED_ACCESS, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

app = Flask(__name__)

db = SQLAlchemy()
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')
# initialize the app with the extension
db.init_app(app)

# JWTManager(app)

model = pickle.load(open('model.pkl', 'rb'))


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


@app.route('/')
def index():
    return {"helloworl": "hello world"}


# @app.route('/test')
# @jwt_required()
# def test():
#     user_id = get_jwt_identity()
#     if user_id:
#         user = User.query.filter_by(id=user_id).first()
#         return jsonify({
#             'username': user.username,
#             'email': user.email
#         }), HTTP_200_OK
#     else:
#         return jsonify({
#             "error": "unauthorized access"
#         }), HTTP_401_UNAUTHORIZED_ACCESS


@app.route('/predict', methods=['POST'])
def predict():
    # Pregnancies	Glucose	BloodPressure	SkinThickness	Insulin	BMI	DiabetesPedigreeFunction	Age
    preganancies = request.get_json().get('pregnancies', '')
    glucose = request.get_json().get('glucose', '')
    blood_pressure = request.get_json().get('blood_pressure', '')
    skin_thickness = request.get_json().get('skin_thickness', '')
    insulin = request.get_json().get('insulin', '')
    bmi = request.get_json().get('bmi', '')
    dpf = request.get_json().get('dpf', '')
    age = request.get_json().get('age', '')

    if preganancies == '':
        return jsonify({'error': 'pregnancy field is empty'})
    elif glucose == '':
        return jsonify({'error': 'Glucose field is empty'})
    elif blood_pressure == '':
        return jsonify({'error': 'BloodPressure field is empty'})
    elif skin_thickness == '':
        return jsonify({'error': 'SkinThickness field is empty'})
    elif insulin == '':
        return jsonify({'error': 'Insulin field is empty'})
    elif bmi == '':
        return jsonify({'error': 'BMI field is empty'})
    elif dpf == '':
        return jsonify({'error': 'DiabetesPedigreeFunction field is empty'})
    elif age == '':
        return jsonify({'error': 'Age field is empty'})
    else:
        dictionary_data = {"Pregnancies": preganancies, "Glucose": glucose, "BloodPressure": blood_pressure,
                           "SkinThickness": skin_thickness, "Insulin": insulin, "BMI": bmi, "DiabetesPedigreeFunction": dpf, "Age": age}

        x_test = pd.DataFrame(dictionary_data, index=[0])
        predict_gbst = model.predict(x_test)
        # result =

        print(predict_gbst)
        return jsonify({'result': predict_gbst.tolist()[0]})


@app.route('/register', methods=['POST'])
def register():
    username = request.get_json().get('username', '')
    useremail = request.get_json().get('email', '')
    password = request.get_json().get('password', '')

    if len(username) < 3:
        return jsonify({'error': 'Username cannot be less than eight characters'}), HTTP_400_BAD_REQUEST

    if len(password) < 8:
        return jsonify({'error': ' Weak password! It cannot be less than eight characters'}), HTTP_400_BAD_REQUEST

    # check if username is alphanumeric
    if not username.isalnum() or " " in username:
        return jsonify({'error': 'Username should be alphanumeric and without space'}), HTTP_400_BAD_REQUEST

    if not validators.email(useremail):
        return jsonify({'error': 'Email is invalid'}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=useremail).first() is not None:
        return jsonify({'error': 'Email already exists'}), HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': 'Username already exists'}), HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)

    user = User(username=username, email=useremail, password=pwd_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': "User registered successfully",
        'user': {
            'username': username, "email": useremail
        }
    }), HTTP_201_CREATED


@app.route('/login', methods=['POST'])
# @swag_from('./docs/auth/login.yaml')
def login():
    useremail = request.get_json().get('email', '')
    password = request.get_json().get('password', '')

    user = User.query.filter_by(email=useremail).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            #     refresh_token = create_refresh_token(identity=user.id)
            #     access_token = create_access_token(identity=user.id)

            return jsonify({
                'user': {
                    # 'refresh': refresh_token,
                    # 'access': access_token,
                    'username': user.username,
                    'email': user.email
                }
            }), HTTP_200_OK
    return jsonify({'error': 'Wrong login details'}), HTTP_401_UNAUTHORIZED_ACCESS

#     {
#     "preganancies": 6,
#     "glucose": 148,
#     "blood_pressure": 72,
#     "skin_thicknesss": 35,
#     "insulin": 0,
#     "bmi": 33.6,
#     "dpf": 0.627,
#     "age": 50
# }


if __name__ == "__main__":
    app.run()
