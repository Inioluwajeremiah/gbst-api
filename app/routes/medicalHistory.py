
from flask import Blueprint, request
from markupsafe import Markup
from app.databaseModel import db, User, MedicalHistory
from app.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST
from flask_login import login_required, current_user

medical_history_blueprint = Blueprint("medical_history", __name__)

@medical_history_blueprint.route("/", methods=["GET", "POST"])
def medical_history ():

    if request.method == "GET":
        pass
    if request.method == "POST":
        
        hypertension = request.json['hypertension']
        diabetes = request.json['diabetes']
        asthma = request.json['asthma']
        chronicLungDisease  = request.json['chronicLungDisease']
        sickleCellDisease = request.json['sickleCellDisease']
        pcos = request.json['pcos']
        diabetesDuration = request.json['diabetesDuration']
        gdm = request.json['gdm']

        hypertension = Markup.escape(hypertension)
        diabetes = Markup.escape(diabetes)
        asthma = Markup.escape(asthma)
        chronicLungDisease = Markup.escape(chronicLungDisease)
        sickleCellDisease = Markup.escape(sickleCellDisease)
        pcos = Markup.escape(pcos)
        diabetesDuration = Markup.escape(diabetesDuration)
        gdm = Markup.escape(gdm)

        if not hypertension:
            return {"message": "Hypertension response required"}
        if not diabetes:
            return {"message": "Diabetes response required"}
        if not asthma:
            return {"message": "Asthma response required"}
        if not chronicLungDisease:
            return {"message": "Chronic Lung Disease response required"}
        if not sickleCellDisease:
            return {"message": "Sickle Cell Disease response required"}
        if not pcos:
            return {"message": "Polycytist Ovary Syndrome response required"}
        if not diabetesDuration:
            return {"message": "Duration of diabetes required"}
        if not gdm:
            return {"message": "Gestaional Diabetes response required"}

        # medicalHistory = MedicalHistory.query.filter_by(user_id=current_user.id).first()
        medicalHistory = MedicalHistory(
            hypertension = hypertension,
            diabetes = diabetes,
            asthma = asthma,
            chronicLungDisease  = chronicLungDisease,
            sickleCellDisease = sickleCellDisease,
            pcos = pcos,
            diabetesDuration = diabetesDuration,
            gdm = gdm,
            user_id=current_user.id
            )
        db.session.add(medicalHistory)
        db.session.commit()
        return {"message": "Data saved successfully!"}, HTTP_200_OK

    return {"message": "Bad request"}, HTTP_400_BAD_REQUEST


    
