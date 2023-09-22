
from flask import Blueprint, request
from markupsafe import Markup
from app.databaseModel import db, User, Enrollment
from app.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST
from flask_login import login_required, current_user


enrollment_blueprint = Blueprint("enrollment", __name__)

@enrollment_blueprint.route("/", methods=["GET", "POST"])
@login_required
def enrollment():

    if request.method == "GET":
        pass
    if request.method == "POST":

        age = request.json['age']
        educationLevel = request.json['educationLevel']
        maritalStatus = request.json['maritalStatus']
        religion = request.json['religion']
        ethnicity = request.json['ethnicity']
        occupation = request.json['occupation']

        age = Markup.escape(age)
        educationLevel = Markup.escape(educationLevel)
        maritalStatus = Markup.escape(maritalStatus)
        religion = Markup.escape(religion)
        ethnicity = Markup.escape(ethnicity)
        occupation = Markup.escape(occupation)


        enrollment = Enrollment(age_at_last_birthday=age, level_of_education = educationLevel,
            marital_status = maritalStatus, religion = religion, ethnicity = ethnicity,
            occupation = occupation, user_id=current_user.id)
        
        db.session.add(enrollment)
        db.session.commit()

        return {"message": "Data saved successfully!"}, HTTP_200_OK
    return {"message": "Bad request"}, HTTP_400_BAD_REQUEST



    
