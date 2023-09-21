
from flask import Blueprint, request

profile_blueprint = Blueprint("profile", __name__)

@profile_blueprint.route("/", methods=["GET", "POST"])
def profile():

    if request.method == "GET":
        pass
    if request.method == "POST":
        pass

    
