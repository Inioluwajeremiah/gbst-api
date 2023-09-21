
from flask import Blueprint, request

exercise_blueprint = Blueprint("exercise", __name__)

@exercise_blueprint.route("/", methods=["GET", "POST"])
def exercise ():

    if request.method == "GET":
        pass
    if request.method == "POST":
        pass

    
