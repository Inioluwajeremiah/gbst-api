
from flask import Blueprint, request

child_birth_outcome_blueprint = Blueprint("child_birth_outcome", __name__)

@child_birth_outcome_blueprint.route("/", methods=["GET", "POST"])
def child_birth_test ():

    if request.method == "GET":
        pass
    if request.method == "POST":
        pass

    
