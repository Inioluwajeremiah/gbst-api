
from flask import Blueprint, request, session
from itsdangerous import URLSafeTimedSerializer
import os
from app.databaseModel import User 
from app import db
from markupsafe import Markup
import validators
from app.status_codes import HTTP_200_OK, HTTP_201_CREATED,\
    HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED_ACCESS, HTTP_404_NOT_FOUND, \
    HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR
import datetime


verify_blueprint = Blueprint("verify", __name__)

# verify user
@verify_blueprint.get('/token/<token>')
def verify_user_token(token):
    serializer = URLSafeTimedSerializer(os.environ.get('SECRET_KEY'))
    try:
        user_email = serializer.loads(token, salt='email-verification', max_age=6000)
       
        # fetch user from database with retrieved email
        user = User.query.filter_by(email=user_email).first()
        # if user does not exist in database
        if user is None:
            return {"message": "User does not exist, kindly Sign up to continue"}, HTTP_404_NOT_FOUND
        
        #  if user is already verified
        if user.is_verified:
            return {"message": "User already verified."}, HTTP_400_BAD_REQUEST
        
        # compare input code and retrieved code
        if user and not user.is_verified:

            # print(input_code ==  user.otp)
            # update user is_verified status in the databse
            user.is_verified = True
            db.session.add(user)
            db.session.commit()
            # delete email from session
            session.pop('email', None)
            return {"message": "User verification successful"},  HTTP_200_OK
    except Exception as e:
         return {"message": f"{e}"}

# verify user using authentication code
@verify_blueprint.route('/code', methods=['POST'])
def verify_user_code():
        # get code and email from form
    email = request.json['email']
    input_code = request.json['code']

    # clean email and code
    email = Markup.escape(email)
    input_code =  Markup.escape(input_code)

    # fetch user from database with retrieved email
    user = User.query.filter_by(email=email).first()
    # if user does not exist in database
    if user is None:
        return {"message": "User does not exist, kindly Sign up to continue"}, HTTP_404_NOT_FOUND
    
    #  if user is already verified
    if user.is_verified:
        return {"message": "User already verified, you can proceed to Signin"}, HTTP_400_BAD_REQUEST
    
    # compare input code and retrieved code
    user_otp = user.otp
    if input_code != user_otp:
        return {"message": "Code does not match"}, HTTP_400_BAD_REQUEST
    
    time_difference = user.expiration_time - datetime.datetime.utcnow()
    
    if time_difference.total_seconds() <= 0:
        return {"message": "token has expired"}
    
    # compare input code and retrieved code
    if user and user_otp == input_code:

        # print(input_code ==  user.otp)
        # update user is_verified status in the databse
        user.is_verified = True
        db.session.add(user)
        db.session.commit()
        # delete email from session
        session.pop('email', None)
        return {"message": "Verification successful!"},  HTTP_200_OK




