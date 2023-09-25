
from flask import Blueprint, request
from markupsafe import Markup
from app.databaseModel import db, ClinicalHistory
from app.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST
from flask_login import login_required, current_user

clinical_history_blueprint = Blueprint("clinical_history", __name__)

@clinical_history_blueprint.route("/", methods=["GET", "POST"])
@login_required
def clinical_history ():

    if request.method == "GET":
        pass
    if request.method == "POST":
        weight = request.json['weight']
        height = request.json['height']
        bmi = request.json['bmi']
        armCircumference = request.json['armCircumference']
        waistCircumference = request.json['waistCircumference']
        hipCircumference = request.json['hipCircumference']
        waistHipCircumference = request.json['waistHipCircumference']
        gestationalAge = request.json['gestationalAge']

        weight = Markup.escape(weight)
        height = Markup.escape(height)
        bmi = Markup.escape(bmi)
        armCircumference = Markup.escape(armCircumference)
        waistCircumference = Markup.escape(waistCircumference)
        hipCircumference = Markup.escape(hipCircumference)
        waistHipCircumference = Markup.escape(waistHipCircumference)
        gestationalAge = Markup.escape(gestationalAge)

        if not weight:
            return {"message": "Weight required"}
        if not height:
            return {"message": "Height required"}
        if not bmi:
            return {"message": "BMI required"}
        if not armCircumference:
            return {"message": "Arm circumference required"}
        if not waistCircumference:
            return {"message": "Waist circumference required"}
        if not hipCircumference:
            return {"message": "Hip circumference required"}
        if not waistHipCircumference:
            return {"message": "Waist-Hip circumference required"}
        if not gestationalAge:
            return {"message": "Gestaional age required"}
        
        clinicalHistory = ClinicalHistory.query.filter_by(user_id=current_user.id).first()

        if clinicalHistory:
            if weight:
                clinicalHistory.weight = weight
                db.session.commit()
            if height:
                clinicalHistory.height = height
                db.session.commit()
            if bmi:
                clinicalHistory.bmi = bmi
                db.session.commit()
            if armCircumference:
                clinicalHistory.armCircumference = armCircumference
                db.session.commit()
            if waistCircumference:
                clinicalHistory.waistCircumference = waistCircumference
                db.session.commit()
            if hipCircumference:
                clinicalHistory.hipCircumference = hipCircumference
                db.session.commit()
            if waistHipCircumference:
                clinicalHistory.waistHipCircumference = waistHipCircumference
                db.session.commit()
            if gestationalAge:
                clinicalHistory.gestationalAge = gestationalAge
                db.session.commit()
            return {"message": "Clinical History saved successfully!"}, HTTP_200_OK
            
        if not clinicalHistory:

            # clinicalHistory = clinicalHistory.query.filter_by(user_id=current_user.id).first()
            clinicalHistory = ClinicalHistory(
                weight = weight,
                height = height,
                bmi = bmi,
                armCircumference  = armCircumference,
                waistCircumference = waistCircumference,
                hipCircumference = hipCircumference,
                waistHipCircumference= waistHipCircumference,
                gestationalAge = gestationalAge,
                user_id=current_user.id
                )
            db.session.add(clinicalHistory)
            db.session.commit()
            return {"message": "Clinical History saved successfully!"}, HTTP_200_OK

    return {"message": "Bad request"}, HTTP_400_BAD_REQUEST

    
