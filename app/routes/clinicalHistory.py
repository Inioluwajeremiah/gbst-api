
from flask import Blueprint, request

clinical_history_blueprint = Blueprint("clinical_history", __name__)

@clinical_history_blueprint.route("/", methods=["GET", "POST"])
def clinical_history ():

    if request.method == "GET":
        pass
    if request.method == "POST":
        pass

    
