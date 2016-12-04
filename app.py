from flask import Flask, request, redirect, render_template
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

######################## REST API ########################

def jwt_is_valid(request):
    secret_key_utf8 = b64encode(app.secret_key).decode('utf-8')
    signed_payload = request.authorization
    try:
        auth_token = jwt.decode(signed_payload, secret_key_utf8)
        if "signing_time" in auth_token and "signing_ip" in auth_token and "user" in auth_token and "access_level" in auth_token:
            signing_time = datetime.fromtimestamp(float(auth_token['signing_time']))
            one_hour_from_signing = signing_time + timedelta(hours=1)
            if datetime.now() < one_hour_from_signing and auth_token["signing_ip"] == str(request.remote_addr):
                return True
    except jwt.DecodeError:
        raise InternalServerError
    return False


def generate_jwt(user, request):
    signingTime = datetime.utcnow()
    payload_id = b64encode(urandom(64)).decode('utf-8')
    secret_key_utf8 = b64encode(app.secret_key).decode('utf-8')
    user.session = payload_id
    user.save()
    jwt_contents = {"user": str(user.uid),
                    "signing_time": signingTime.strftime("%s"),
                    "signing_ip": str(request.remote_addr)}
    encoded_token = jwt.encode(jwt_contents, secret_key_utf8, algorithm='HS256')
    return encoded_token

def get_user(request):
    auth_token = get_jwt_contents(request)
    user = None

    try:
        user = User.get(User.uid == auth_token["user"])
    except:
        raise InternalServerError

    return user

def get_jwt_contents(request):
    # Decorators beforehand ensure that we can do this safely.
    secret_key_utf8 = b64encode(app.secret_key).decode('utf-8')
    signed_payload = request.cookies.get("presence")
    auth_token = jwt.decode(signed_payload, secret_key_utf8)
    return auth_token

def requires_token_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not jwt_is_valid(request):
            raise Forbidden
        return f(*args, **kwargs)

    return decorated

class Login(Resource):
    def post(self):
        try:
            user = User.get(User.email == request.form["email"])
        except:
            raise InternalServerError

class Register(Resource):
    def post(self):
        user = User.create(uid=uuid4(),
                               email=request.form["email"],
                               username=request.form["username"],
                               password=request.form["pass"])
        user.save()
        return "Successfully created user."
        


api.add_resource(Login, '/login')
api.add_resource(Register, '/register')


if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=80)