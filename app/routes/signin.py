
from flask import Blueprint, request

signin_blueprint = Blueprint("signin", __name__)

@signin_blueprint.route("/", methods=["GET", "POST"])
def signin():

    if request.method == "GET":
        pass
    if request.method == "POST":
        pass

    
