from flask import Blueprint
from flask import session
from flask import g
from flask import request
from flask import render_template


bp = Blueprint("login", __name__)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    
    else: print("usuario logeado")

@bp.route("/register", methods = ("GET", "POST"))
def register():
    #cuando se envia el formulario de registro
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

    return render_template("register.html")

@bp.route("/login", methods = ("GET", "POST"))
def login():
    #cuando se envia el formulario de inicio de sesion
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

    return render_template("login.html")