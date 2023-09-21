
from flask import Blueprint, request

medical_history_blueprint = Blueprint("medical_history", __name__)

@medical_history_blueprint.route("/", methods=["GET", "POST"])
def medical_history ():

    if request.method == "GET":
        pass
    if request.method == "POST":
        pass

    
