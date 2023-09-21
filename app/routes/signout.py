
from flask import Blueprint, request

signout_blueprint = Blueprint("signout", __name__)

@signout_blueprint.route("/", methods=["GET", "POST"])
def signout():

    if request.method == "GET":
        pass
    if request.method == "POST":
        pass

    
