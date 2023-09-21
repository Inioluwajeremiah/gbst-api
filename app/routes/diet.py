
from flask import Blueprint, request

diet_blueprint = Blueprint("diet", __name__)

@diet_blueprint.route("/", methods=["GET", "POST"])
def diet ():

    if request.method == "GET":
        pass
    if request.method == "POST":
        pass

    
