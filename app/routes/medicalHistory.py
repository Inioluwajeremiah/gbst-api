
from flask import Blueprint, request
from markupsafe import Markup
from app.databaseModel import db, MedicalHistory
from app.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST
from flask_login import login_required, current_user

medical_history_blueprint = Blueprint("medical_history", __name__)

@medical_history_blueprint.route("/", methods=["GET", "POST"])
@login_required
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
        history = request.json['history']

        hypertension = Markup.escape(hypertension)
        diabetes = Markup.escape(diabetes)
        asthma = Markup.escape(asthma)
        chronicLungDisease = Markup.escape(chronicLungDisease)
        sickleCellDisease = Markup.escape(sickleCellDisease)
        pcos = Markup.escape(pcos)
        diabetesDuration = Markup.escape(diabetesDuration)
        gdm = Markup.escape(gdm)
        history = Markup.escape(history)

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
        if not history:
            return {"message": "History of Gestational Diabetes Mellitus in your family is required"}
        
         # if fields are not cimpuslory only comment out the codes above
        
        medicalHistory = MedicalHistory.query.filter_by(user_id=current_user.id).first()

        if medicalHistory:
            if hypertension:
                medicalHistory.hypertension = hypertension
                db.session.commit()
            if diabetes:
                medicalHistory.diabetes = diabetes
                db.session.commit()
            if asthma:
                medicalHistory.asthma = asthma
                db.session.commit()
            if chronicLungDisease:
                medicalHistory.chronicLungDisease = chronicLungDisease
                db.session.commit()
            if sickleCellDisease:
                medicalHistory.sickleCellDisease = sickleCellDisease
                db.session.commit()
            if pcos:
                medicalHistory.pcos = pcos
                db.session.commit()
            if diabetesDuration:
                medicalHistory.diabetesDuration = diabetesDuration
                db.session.commit()
            if gdm:
                medicalHistory.gdm = gdm
                db.session.commit()
            if history:
                medicalHistory.history = history
                db.session.commit()
            return {"message": "Medical History saved successfully!"}, HTTP_200_OK
            
        if not medicalHistory:

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
                history = history,
                user_id=current_user.id
                )
            db.session.add(medicalHistory)
            db.session.commit()
            return {"message": "Medical History saved successfully!"}, HTTP_200_OK

    return {"message": "Bad request"}, HTTP_400_BAD_REQUEST


    
