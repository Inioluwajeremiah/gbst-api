
from flask import Blueprint, request
from markupsafe import Markup
from app.databaseModel import db, ChildBirthOutcome
from app.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST
from flask_login import login_required, current_user

child_birth_outcome_blueprint = Blueprint("child_birth_outcome", __name__)

@child_birth_outcome_blueprint.route("/", methods=["GET", "POST"])
@login_required
def child_birth_test ():

    if request.method == "GET":
        pass

    if request.method == "POST":
        deliverymode = request.json['deliverymode']
        weight = request.json['weight']
        childbirthOutcome = request.json['childbirthOutcome']
        bloodSugar = request.json['bloodSugar']
        bloodSugarAfterSixweeks = request.json['bloodSugarAfterSixweeks']

        deliverymode = Markup.escape(deliverymode)
        weight = Markup.escape(weight)
        childbirthOutcome = Markup.escape(childbirthOutcome)
        bloodSugar = Markup.escape(bloodSugar)
        bloodSugarAfterSixweeks = Markup.escape(bloodSugarAfterSixweeks)

        if not deliverymode:
            return {"message": "Mode of delivery required"}
        if not weight:
            return {"message": "Weight required"}
        if not childbirthOutcome:
            return {"message": "Outcome of childbirth required"}
        if not bloodSugar:
            return {"message": "Blood sugar result after birth required"}
        if not bloodSugarAfterSixweeks:
            return {"message": "Blood sugar result six weeks after birth required"}
        
         # if fields are not cimpuslory only comment out the codes above
        
        childBirthOutcome = ChildBirthOutcome.query.filter_by(user_id=current_user.id).first()

        if childBirthOutcome:
            if deliverymode:
                childBirthOutcome.deliverymode = deliverymode
                db.session.commit()
            if weight:
                childBirthOutcome.weight = weight
                db.session.commit()
            if childbirthOutcome:
                childBirthOutcome.childbirthOutcome = childbirthOutcome
                db.session.commit()
            if bloodSugar:
                childBirthOutcome.bloodSugar = bloodSugar
                db.session.commit()
            if bloodSugarAfterSixweeks:
                childBirthOutcome.bloodSugarAfterSixweeks = bloodSugarAfterSixweeks
                db.session.commit()
            return {"message": "Outcome of childbirth saved successfully!"}, HTTP_200_OK
            
        if not childBirthOutcome:

            # childBirthOutcome = childBirthOutcome.query.filter_by(user_id=current_user.id).first()
            childBirthOutcome = ChildBirthOutcome(
                deliverymode = deliverymode,
                weight = weight,
                childbirthOutcome = childbirthOutcome,
                bloodSugar  = bloodSugar,
                bloodSugarAfterSixweeks = bloodSugarAfterSixweeks,
                user_id=current_user.id
                )
            db.session.add(childBirthOutcome)
            db.session.commit()
            return {"message": "Outcome of childbirth saved successfully!"}, HTTP_200_OK

    return {"message": "Bad request"}, HTTP_400_BAD_REQUEST

    
