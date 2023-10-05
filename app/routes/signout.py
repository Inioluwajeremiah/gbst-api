
from flask import Blueprint, request
from werkzeug.security import check_password_hash
from markupsafe import Markup
from app.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED_ACCESS
from app.databaseModel import db, User
from flask_login import  login_user, logout_user, login_required

signout_blueprint = Blueprint("signout", __name__)

@signout_blueprint.get("/")
@login_required
def signout():
    logout_user()
    return {"messsage": "Logout successfull!"}


    
