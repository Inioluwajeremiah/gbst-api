
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from markupsafe import Markup
from app.databaseModel import db, Profile, User
from app.routes.signup import is_valid_password, sendEmail, generate_random_code
from app.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST
from flask_login import login_required, current_user, logout_user
from werkzeug.utils import secure_filename
import os
profile_blueprint = Blueprint("profile", __name__)
import validators
import datetime

# Function to check if the uploaded file has an allowed extension
def allowed_file(filename):
    allowed_extensions = {'jpg', 'jpeg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@profile_blueprint.post("/upload_picture")
@login_required
def upload_picture():
    file = request.files['file']
    profile = Profile.query.filter_by(user_id=current_user.id).first()

    if file and allowed_file(file.filename):
        if file.content_length > current_app.config['MAX_CONTENT_LENGTH']:
            return jsonify(error='File size exceeds the limit (1 MB)'), HTTP_400_BAD_REQUEST

        filename = secure_filename(file.filename)
        file_extension = os.path.splitext(filename)[1]
        new_name = "gbstaiapp_image" + str(current_user.id) + file_extension 
        # file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        file.save('/home/gbstaiapp/gbst-api/static/profile_image/'+ new_name)
        path = os.path.join(current_app.config['UPLOAD_FOLDER']) + '/' + new_name
        profile_picture_uri = f"https://www.pythonanywhere.com/user/gbstaiapp/files/home/gbstaiapp/gbst-api/static/profile_image/{new_name}"
        if profile:
            profile.profile_picture = profile_picture_uri
            db.session.commit()
            return {"message":'File successfully uploaded.', 
                "uri":profile_picture_uri,
                "local_path": path
                }, HTTP_200_OK
        
        if not profile:
            profile = Profile(profile_picture = profile_picture_uri, user_id=current_user.id)
            db.session.add(profile)
            db.session.commit() 
            return {"message":'File successfully uploaded.', 
                "uri":profile_picture_uri,
                "local_path": path
                 }, HTTP_200_OK


    return jsonify(error='Invalid file format.'), HTTP_400_BAD_REQUEST


@profile_blueprint.post("/change_password")
@login_required
def change_password():
    oldPassword = request.json['oldPassword']
    newPassword = request.json['newPassword']

    oldPassword =  Markup.escape(oldPassword)
    newPassword =  Markup.escape(newPassword)

    if not oldPassword:
        return {"message": "Old password is required"}, HTTP_400_BAD_REQUEST
    if not is_valid_password(newPassword):
        return {"message": "New password is invalid, consider using a strong password"}, HTTP_400_BAD_REQUEST
    
    user = User.query.filter_by(id=current_user.id).first()
    # hash user password
    is_old_password_correct = check_password_hash(user.password, oldPassword)

    if is_old_password_correct:
        # hash user password
        new_password_hashed = generate_password_hash(newPassword)

        user.password = new_password_hashed
        db.session.commit()
        return {"message": "Password updated successfully!", "pass": is_old_password_correct, "new": newPassword}, HTTP_200_OK
    return {"message": "Old password incorrect"}, HTTP_400_BAD_REQUEST


@profile_blueprint.post('/change_email')
@login_required
def change_email():

    new_email = request.json['new_email']
    
    new_email = Markup.escape(new_email)

    if not validators.email(new_email):
        return {"message":"Invalid email address"}, HTTP_400_BAD_REQUEST
    
    user = User.query.filter_by(id=current_user.id).first()

    if user:
        # expiration time
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=3)
        # generateotp
        otp = generate_random_code()
        # send authentication code to user
        sendEmail(new_email)

        # update user table
        user.email = new_email
        user.otp = otp
        user.expiration_time = expiration_time
        user.is_verified = False
        db.session.commit()
        logout_user()

        return {"message": f"Change of user email successfull. Verification code has been sent to {new_email}."}

    

# get user full name
@profile_blueprint.get('/fullname')
@login_required
def fullname():

    user = User.query.filter_by(id=current_user.id).first()
    if user:
        return {"fullname":user.fullname,'email':user.email}


