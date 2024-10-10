from flask import Blueprint
from flask import session
from flask import g
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from .db import get_db
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

bp = Blueprint("login", __name__)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    
    else: print("usuario logeado")


#TODO hacer el registro
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
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM usuarios where email = ?", (email,)
        ).fetchone()

        if user is None:
            error = "Correo incorrecto"
        elif not check_password_hash(user["password"], password):
            error = "Contraseña incorrecta"

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))
    

    return render_template("login.html")

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))