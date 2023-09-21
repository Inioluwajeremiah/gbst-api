
from flask import Blueprint, request

blood_sugar_test_blueprint = Blueprint("blood_sugar_test", __name__)

@blood_sugar_test_blueprint.route("/", methods=["GET", "POST"])
def blood_sugar_test ():

    if request.method == "GET":
        pass
    if request.method == "POST":
        pass

    
