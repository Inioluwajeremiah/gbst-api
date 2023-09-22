
from flask import Blueprint, request
from werkzeug.security import check_password_hash
from markupsafe import Markup
from app.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED_ACCESS
from app.databaseModel import db, User
from flask_login import  login_user

signin_blueprint = Blueprint("signin", __name__)

@signin_blueprint.route("/", methods=["POST"])
def signin():

    email = request.json['email']
    password = request.json['password']

    email = Markup.escape(email)
    password = Markup.escape(password)
    
    if request.method == "POST":
        user = User.query.filter_by(email=email).first()

        if not user:
            return {"message": "User not found. Sign up to continue"}, HTTP_401_UNAUTHORIZED_ACCESS

        # check if user is signed up but not authenticate
        if user and not user.is_verified:
            return {"message": "User not yet verified"}, HTTP_401_UNAUTHORIZED_ACCESS
        
        if user and user.is_verified:
            is_password_correct = check_password_hash(user.password, password)
            if is_password_correct:
                login_user(user)
                return{'message': 'Login successful!'}, HTTP_200_OK
            else:
                return {"message": "Incorrect password"}, HTTP_401_UNAUTHORIZED_ACCESS
        return {"message": "User does not exist"}, HTTP_400_BAD_REQUEST
        
        
 

    
