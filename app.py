from flask import Flask, request, redirect, render_template, url_for, session
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from werkzeug.utils import secure_filename
from os import urandom, path
from uuid import uuid4
from functools import wraps
from datetime import datetime

from models import *

app = Flask(__name__)

UPLOAD_FOLDER = '/home/markrjr/uploads'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])

app.secret_key = urandom(64)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION_USE_SIGNER'] = True


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

######################## ROUTES ########################

@app.route('/')
def index():
    USERNAME = ""
    if 'user' in session:
        USERNAME = session["user"]["username"]
    return render_template("index.html", USERNAME=USERNAME)

@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html", USERNAME=session["user"]["username"])

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(url_for('generic_error', error="UPLOAD_FAILURE"))
        file = request.files['file']
        # if user does not select file,ater. browser also
        # submit a empty part without filename
        if file.filename == '':
            return redirect(url_for('generic_error', error="UPLOAD_FAILURE"))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(path.join(app.config['UPLOAD_FOLDER'], filename))
            uploaded = File.create(name=request.form["name"],
                            date_uploaded=datetime.utcnow(),
                            semester=request.form["semester"],
                            uploaded_by=session["email"],
                            grade=request.form["grade"],
                            server_name=file.filename)
            uploaded.save()
            file_rating = Rating.create()
            uploaded.rating = file_rating
            uploaded.save()
            return redirect(url_for('profile'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/error/<error>')
def generic_error(error):
    message = "We're not quite sure what happened, but we're already on it."
    if error == "INVALID_PASS":
        message = "Please check your password and try again."
    elif error == "EMAIL_DOES_NOT_EXIST":
        message = "We couldn't find a user with that email."
    elif error == "UPLOAD_FAILURE":
        message = "Something went wrong while trying to uploading that file, please try again later."
    return render_template("generic.html", MESSAGE_TYPE="That's an error.", MESSAGE=message)

@app.route('/success/<success>')
def generic_message(success):
    message = "Thanks."
    if success == "SIGNUP_SUCCESS":
        message = "Thanks for signing up for StuddyBuddy!"
    return render_template("generic.html", MESSAGE_TYPE="Woohoo!", MESSAGE=message)

@app.route('/login', methods=["POST"])
def login():
    user = None
    try:
        user = User.get(User.email == request.form["email"])
        if user.password == request.form["pass"]:
            user = {"email" : user.email, "username" : user.username}
            session["user"] = user
            return redirect("/profile")
        else:
            return redirect(url_for('generic_error', error="INVALID_PASS"))
    except DoesNotExist:
        return redirect(url_for('generic_error', error="EMAIL_DOES_NOT_EXIST"))

@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect('/')

@app.route('/register', methods=["POST"])
def register():
    user = User.create(uid=uuid4(),
                            email=request.form["email"],
                            username=request.form["username"],
                            password=request.form["pass"])
    user.save()
    user_dict = {"email" : user.email, "username" : user.username}
    session["user"] = user_dict
    return redirect(url_for('generic_message', success="SIGNUP_SUCCESS"))

@app.route('/search', methods=["POST"])
def search():
    return str(request.form["search_term"])

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=80)