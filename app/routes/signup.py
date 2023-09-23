from flask import Blueprint, request, url_for
from werkzeug.security import generate_password_hash
from markupsafe import Markup
import validators
from app.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
import random
from app.databaseModel import db, User
from app import mail
from flask_mail import Message
import datetime
from itsdangerous import URLSafeTimedSerializer
import os


# Create the blueprint instance
signup_blueprint = Blueprint('signup', __name__)


# validate password
def is_valid_password(password):
    # Define your password validation criteria
    min_length = 8
    contains_uppercase = any(char.isupper() for char in password)
    contains_lowercase = any(char.islower() for char in password)
    contains_digit = any(char.isdigit() for char in password)
    contains_special = any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?~' for char in password)

    return (
        len(password) >= min_length and
        contains_uppercase and
        contains_lowercase and
        contains_digit and
        contains_special
    )

# generate 6 digits code
def generate_random_code():
    return random.randint(1000, 9999)

# send code to email
def sendEmail(eml, code):
    serializer = URLSafeTimedSerializer(os.environ.get('SECRET_KEY'))
    token = serializer.dumps(eml, salt='email-verification')
    # Create a verification link
    verification_link = url_for('verify.verify_user_token', token=token, _external=True)
    msg = Message("Authentication Code", recipients=[eml])
    
    # msg.html = f"<div style='padding:8px; background-color:#2563eb; color:#f5f5f5; font-weight:bold; border-radius:20px;'> \
    #                 <h3 style='padding:5px 2px; text-align:center; color:#f5f5f5;'>SIWES Authentication Code</h3> \
    #                 <p style='color:#f5f5f5;'>Here is your authentication code for SIWES. <br/> <b>NB:</b> \
    #                 Code expires in 10 mins.</p> \
    #                 <h4 style='text:center; letter-spacing:5px;'>{code}</h4> \
    #                 <p style='padding:5px; color:#fff;'>or visit this link for verficaation: {verification_link}</p> \
    #             <div>" 

# data:image/jpeg;base64,{encoded_logo}
    # Read and encode the image
    # with open("/logo.png", 'rb') as virtual_church_logo:
    #     encoded_logo = base64.b64encode(virtual_church_logo.read()).decode('utf-8')

    logo_url = "https://firebasestorage.googleapis.com/v0/b/gbst-cc5c3.appspot.com/o/icon3.png?alt=media&token=0e87eed5-9ea1-4fa7-8b46-0fd0a10b9c81"
    msg.html = f"""
                <div style='background-color:#f0efef; padding: 2rem 1rem;'>
                    <div style='background-color:#fff; max-width:32rem; width:90%; margin: 2rem auto; padding: 2rem 1rem'> 
                        <div style='display:flex; align-items:center; justify-items:center;'>
                            <img src={logo_url} alt="virtual church logo" style="width:5rem; height:5rem;"/>
                            <h1> <a href="" style='color:#66CA98; font-size:1.5em;'>GBST</a></h1>
                        </div>
                        <h3 style='padding:5px 2px; font-size:2em'>Verify your Account</h3> 
                        <p style='font-size:1.2em;'>Thank you for signing up to GBST. Your health is our priority!</p> 
                        <h4 style="letter-spacing:5px; font-size:4em;">{code}</h4> 
                        <button style='padding:1rem 2rem; outline:none; border:none; border-radius:5px; background-color:#66CA98;'><a href="" style='text:center; color:#fff; font-size:1.2em; font-weight:bold;'>Verify</a></button>
                        <p style='padding:5px; background-color:#f5f5f5; color:#000;'>or visit this link for verfication: {verification_link}</p> 
                        
                    </div>
                </div>
            """
    # msg.body = f"{code}"
        # send auth code to email
    mail.send(msg)

# home
@signup_blueprint.post('/')
def signup():
    fullname = request.json['fullname']
    email = request.json['email']
    password = request.json['password']

    # clean input
    fullname = Markup.escape(fullname)
    email = Markup.escape(email)
    password =  Markup.escape(password)

    if not fullname:
        return {"message": "Fullname is required"}, HTTP_400_BAD_REQUEST
    if not email:
        return {"message": "Email is required"}, HTTP_400_BAD_REQUEST
    if not password:
        return {"message": "Password is required"}, HTTP_400_BAD_REQUEST

    user_verified = User.query.filter_by(email=email, is_verified=True).first()
    user_but_not_verified = User.query.filter_by(email=email, is_verified=False).first()

    if not validators.email(email):
        return {"message":"Invalid email address"}, HTTP_400_BAD_REQUEST

    if user_verified:
        return {"message": "User already exists, kindly login to your account"}, HTTP_400_BAD_REQUEST
    if user_but_not_verified:
        return {"message": "User already signed up but not verified"}, HTTP_400_BAD_REQUEST
    
    if not is_valid_password(password):
        return {"message": "Invalid password"}, HTTP_400_BAD_REQUEST
    
    # hash user password
    hashed_password = generate_password_hash(password)

    # expiration time
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=3)
    # generateotp
    otp = generate_random_code()
    # send authentication code to user
    try:
        sendEmail(email, otp)
            # add user to database
        user = User(email=email, password=hashed_password, otp=otp, expiration_time=expiration_time)
        db.session.add(user)
        db.session.commit()
        return {"message": "Authentication code sent to user email"}, HTTP_200_OK
    except Exception as e:
            return {"message": f"error sending authentication code. Reason: {e}"}, HTTP_500_INTERNAL_SERVER_ERROR
    

# resend verification code
@signup_blueprint.route('/resend_code', methods=['POST'])
def resend_code():

    email = request.json['email']

    user_verified = User.query.filter_by(email=email, is_verified=True).first()
    user = User.query.filter_by(email=email, is_verified=False).first()

    if user_verified:
        return {"message": "User already verified"}, HTTP_409_CONFLICT
    if not user:
        return {"message": "User not found"}, HTTP_404_NOT_FOUND
    if user:
        # expiration time
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=3)
        otp = generate_random_code()
        user.otp = otp
        user.expiration_time = expiration_time

        db.session.add(user)
        db.session.commit()
        sendEmail(email, otp)
        return {"message": f"Authentication code sent to {email}"}
    
          

# #test data
# "firstname":"firstname",
# "middlename":"middlename",
# "lastname":"lastname",
# "username":"username",
# "email":"email",
# "gender":"gender",
# "birthdate":"2023-09-25",
# "department":"Welfare",
# "marital_status":"single",
# "address":"address",
# "state":"Abuja",
# "country":"Nigeria",
# "branch":"branch",
# "password":"Password#",
# "role":"role"