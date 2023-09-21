
from flask import Blueprint, request

fetal_kick_count_blueprint = Blueprint("fetal_kick_count", __name__)

@fetal_kick_count_blueprint.route("/", methods=["GET", "POST"])
def fetal_kick_count ():

    if request.method == "GET":
        pass
    if request.method == "POST":
        pass

    
