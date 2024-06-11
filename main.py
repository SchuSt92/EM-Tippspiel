from flask import Blueprint

main = Blueprint("main", __name__)

@main.route("/", methods=["GET"])
def home():
    return "Home - Page"

@main.route("/rangliste", methods=["GET"])
def rangliste():
    return "Home - Info"

@main.route("/info", methods=["GET"])
def info():
    return "Home - Info"

@main.route("/spielplan", methods=["GET"])
def spielplan():
    return "Home - Info"