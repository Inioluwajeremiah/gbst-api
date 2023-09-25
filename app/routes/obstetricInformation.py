
from flask import Blueprint, request
from markupsafe import Markup
from app.databaseModel import db, ObstetricInformation
from app.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST
from flask_login import login_required, current_user

obstetric_information_blueprint = Blueprint("obstetric_information", __name__)

@obstetric_information_blueprint.route("/", methods=["GET", "POST"])
def obstetric_information ():

    if request.method == "GET":
        pass
    if request.method == "POST":
        noOfPregnancies = request.json['noOfPregnancies']
        noOfMiscarriages = request.json['noOfMiscarriages']
        noOfVoluntaryPregnacyTermination = request.json['noOfVoluntaryPregnacyTermination']
        noOfChildbirthDeliveries = request.json['noOfChildbirthDeliveries']
        fourKgBirthWeight = request.json['fourKgBirthWeight']
        anyStillbirth = request.json['anyStillbirth']
        cogenitalMalformation = request.json['cogenitalMalformation']
        lastTimeOFMenstralPeriod = request.json['lastTimeOFMenstralPeriod']
        gestationalAge = request.json['gestationalAge']

        noOfPregnancies = Markup.escape(noOfPregnancies)
        noOfMiscarriages = Markup.escape(noOfMiscarriages)
        noOfVoluntaryPregnacyTermination = Markup.escape(noOfVoluntaryPregnacyTermination)
        noOfChildbirthDeliveries = Markup.escape(noOfChildbirthDeliveries)
        fourKgBirthWeight = Markup.escape(fourKgBirthWeight)
        anyStillbirth = Markup.escape(anyStillbirth)
        cogenitalMalformation = Markup.escape(cogenitalMalformation)
        lastTimeOFMenstralPeriod = Markup.escape(lastTimeOFMenstralPeriod)
        gestationalAge = Markup.escape(gestationalAge)

        if not noOfPregnancies:
            return {"message": "Number of previous pregnancies required"}
        if not noOfMiscarriages:
            return {"message": "Number of miscarriages required"}
        if not noOfVoluntaryPregnacyTermination:
            return {"message": "No of voluntary pregnacy termination required"}
        if not noOfChildbirthDeliveries:
            return {"message": "Number of child deliveries required"}
        if not fourKgBirthWeight:
            return {"message": "Response for baby with a birth weight of 4kg and above required"}
        if not anyStillbirth:
            return {"message": "Response for pregnacy that resulted in a stillbirth required"}
        if not cogenitalMalformation:
            return {"message": "Response for child born with cogenital malformation required"}
        if not lastTimeOFMenstralPeriod:
            return {"message": "Last time of menstral period required"}
        if not gestationalAge:
            return {"message": "Gestaional age required"}
        
        obstetricInformation = ObstetricInformation.query.filter_by(user_id=current_user.id).first()

        if obstetricInformation:
            if noOfPregnancies:
                obstetricInformation.noOfPregnancies = noOfPregnancies
                db.session.commit()
            if noOfMiscarriages:
                obstetricInformation.noOfMiscarriages = noOfMiscarriages
                db.session.commit()
            if noOfVoluntaryPregnacyTermination:
                obstetricInformation.noOfVoluntaryPregnacyTermination = noOfVoluntaryPregnacyTermination
                db.session.commit()
            if noOfChildbirthDeliveries:
                obstetricInformation.noOfChildbirthDeliveries = noOfChildbirthDeliveries
                db.session.commit()
            if fourKgBirthWeight:
                obstetricInformation.fourKgBirthWeight = fourKgBirthWeight
                db.session.commit()
            if anyStillbirth:
                obstetricInformation.anyStillbirth = anyStillbirth
                db.session.commit()
            if cogenitalMalformation:
                obstetricInformation.cogenitalMalformation = cogenitalMalformation
                db.session.commit()
            if gestationalAge:
                obstetricInformation.gestationalAge = gestationalAge
                db.session.commit()
            return {"message": "Obstetric Information saved successfully!"}, HTTP_200_OK
            
        if not obstetricInformation:

            # obstetricInformation = obstetricInformation.query.filter_by(user_id=current_user.id).first()
            obstetricInformation = ObstetricInformation(
                noOfPregnancies = noOfPregnancies,
                noOfMiscarriages = noOfMiscarriages,
                noOfVoluntaryPregnacyTermination = noOfVoluntaryPregnacyTermination,
                noOfChildbirthDeliveries  = noOfChildbirthDeliveries,
                fourKgBirthWeight = fourKgBirthWeight,
                anyStillbirth = anyStillbirth,
                cogenitalMalformation= cogenitalMalformation,
                gestationalAge = gestationalAge,
                user_id=current_user.id
                )
            db.session.add(obstetricInformation)
            db.session.commit()
            return {"message": "Obstetric Information saved successfully!"}, HTTP_200_OK

    return {"message": "Bad request"}, HTTP_400_BAD_REQUEST


    
