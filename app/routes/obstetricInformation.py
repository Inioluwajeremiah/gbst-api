
from flask import Blueprint, request

obstetric_information_blueprint = Blueprint("obstetric_information", __name__)

@obstetric_information_blueprint.route("/", methods=["GET", "POST"])
def obstetric_information ():

    if request.method == "GET":
        pass
    if request.method == "POST":
        pass

    
