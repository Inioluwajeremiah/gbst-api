
from flask import Blueprint, request, jsonify, current_app
from markupsafe import Markup
from app.databaseModel import db, Profile
from app.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
profile_blueprint = Blueprint("profile", __name__)

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
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        path = os.path.join(current_app.config['UPLOAD_FOLDER']) + '/' + filename
        profile_picture_uri = f"https://www.pythonanywhere.com/user/gbstaiapp/files/home/gbstaiapp/gbst-api/profile_image/{filename}"
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


@profile_blueprint.get("/change_password")
@login_required
def change_password():
    pass



