from flask import Flask, request, redirect, render_template, url_for, session, send_from_directory
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from werkzeug.utils import secure_filename
from os import urandom, path, remove
from functools import wraps
from datetime import datetime
from re import sub

from models import *

app = Flask(__name__)

UPLOAD_FOLDER = '/home/markrjr/StuddyBuddy/uploads/'
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

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    USERNAME = ""
    if 'user' in session:
        USERNAME = session["user"]["username"]
    return render_template("index.html", USERNAME=USERNAME)

@app.route('/profile')
@login_required
def profile():
    user_files = []
    for a_file in User_File.select():
        if a_file.uploaded_by == session["user"]["email"]:
            user_files.append(a_file)
    if not user_files:
        user_files = None
    return render_template("profile.html", USERNAME=session["user"]["username"], 
                                           USER_EMAIL=session["user"]["email"], 
                                           CURRENT_DATE=datetime.utcnow().strftime("%b %d, %Y"),
                                           USER_FILES=user_files)
                                        
@app.route('/assignment/<file_id>')
def assignment(file_id):
    try:
        a_file = User_File.get(User_File.id == file_id)
        if path.isfile(UPLOAD_FOLDER + a_file.server_name):
            return render_template("file.html", USER_FILE=a_file)
        else:
            return redirect(url_for('generic_error', error="NO_FILES_FOUND"))
    except:
        return redirect(url_for('generic_error', error="NO_FILES_FOUND"))

@app.route('/uploads/<file_name>')
def static_proxy(file_name):
  # send_static_file will guess the correct MIME type
  return send_from_directory(UPLOAD_FOLDER, file_name)

@app.route('/upload', methods=['POST'])
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
            without_extension = filename.split(".")
            filename = sub(r'\W+', '', without_extension[0])
            filename = filename + "." + without_extension[1]
            file.save(path.join(app.config['UPLOAD_FOLDER'], filename))
            uploaded = User_File.create(name=request.form["assignment-name"],
                            date_uploaded=datetime.utcnow().strftime("%b %d, %Y"),
                            semester=request.form["semester"],
                            uploaded_by=session["user"]["email"],
                            grade=request.form["grade"],
                            server_name=filename)
            uploaded.save()
            file_rating = Rating.create()
            uploaded.rating = file_rating
            uploaded.save()
            return redirect(url_for('profile'))
        
@app.route('/delete', methods=["POST"])
@login_required
def delete():
    for a_file in User_File.select():
        if a_file.server_name == request.form["file-to-delete"]:
            remove(UPLOAD_FOLDER + a_file.server_name)
            a_file.delete_instance(recursive=True)
            return redirect(url_for('generic_message', success="FILE_DELETE_SUCCESS"))
        else:
            return redirect(url_for('generic_error', error="FILE_DELETE_FAILURE"))

@app.route('/error/<error>')
def generic_error(error):
    message = "We're not quite sure what happened, but we're already on it."
    if error == "INVALID_PASS":
        message = "Please check your password and try again."
    elif error == "EMAIL_DOES_NOT_EXIST":
        message = "We couldn't find a user with that email."
    elif error == "UPLOAD_FAILURE":
        message = "Something went wrong while trying to uploading that file, please try again later."
    elif error == "FILE_DELETE_FAILURE":
        message = "Something went wrong while trying to delete that file, please try again later."
    elif error == "NO_FILES_FOUND":
        message = "We couldn't find the test or quiz you were searching for."
    return render_template("generic.html", MESSAGE_TYPE="That's an error.", MESSAGE=message)

@app.route('/success/<success>')
def generic_message(success):
    message = "Thanks."
    if success == "SIGNUP_SUCCESS":
        message = "Thanks for signing up for StuddyBuddy!"
    elif success == "FILE_DELETE_SUCCESS":
        message = "Successfully deleted file."
    return render_template("generic.html", MESSAGE_TYPE="Woohoo!", MESSAGE=message)

@app.route('/login', methods=["POST"])
def login():
    user = None
    try:
        user = Uploader.get(Uploader.email == request.form["email"])
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
    user = Uploader.create(email=request.form["email"],
                            username=request.form["username"],
                            password=request.form["pass"])
    user.save()
    user_dict = {"email" : user.email, "username" : user.username}
    session["user"] = user_dict
    return redirect(url_for('generic_message', success="SIGNUP_SUCCESS"))

@app.route('/search', methods=["POST"])
def search():
    list_of_files = []
    search_term = request.form["search_term"]
    for school in University.select():
        if search_term == school.name:
            for a_file in User_File.select():
                if a_file.course and a_file.course.school.id == school.id:
                    list_of_files.append(a_file)
                    search_term = "Files for " + school.name
    for course in Course.select():
        if search_term == course.name:
            for a_file in User_File.select():
                if a_file.course.id == course.id:
                    list_of_files.append(a_file)
                    search_term = "Files for " + course.name
    if not list_of_files:
        for a_file in User_File.select():
            if search_term in a_file.name or search_term == a_file.name:
                list_of_files.append(a_file)
    return render_template("search.html", SEARCH_TERM=search_term, FILES=list_of_files)

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=80)
