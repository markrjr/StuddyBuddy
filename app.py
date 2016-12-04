from flask import Flask, request, redirect, render_template, url_for
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from os import urandom
from uuid import uuid4

from models import *

app = Flask(__name__)
api = Api(app)

app.secretkey = urandom(64)

######################## ROUTES ########################

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/profile')
def profile():
    return render_template("index.html")

@app.route('/error/<error>')
def generic_error(error):
    message = "We're not quite sure what happened, but we're already on it."
    if error == "INVALID_PASS":
        message = "Please check your password and try again."
    elif error == "EMAIL_DOES_NOT_EXIST":
        message = "We couldn't find a user with that email."
    return render_template("error.html", MESSAGE=message)

@app.route('/login', methods=["POST"])
def login():
    user = None
    try:
        user = User.get(User.email == request.form["email"])
        if user.password == request.form["pass"]:
            return "Success", 200
        else:
            return redirect(url_for('generic_error', error="INVALID_PASS"))
    except DoesNotExist:
        return redirect(url_for('generic_error', error="EMAIL_DOES_NOT_EXIST"))

@app.route('/register', methods=["POST"])
def register():
    user = User.create(uid=uuid4(),
                            email=request.form["email"],
                            username=request.form["username"],
                            password=request.form["pass"])
    user.save()
    return "Successfully created user."


######################## REST API ########################


if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=80)