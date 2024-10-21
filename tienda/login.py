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
from flask import flash
from psycopg2 import IntegrityError
from flask import current_app

bp = Blueprint("login", __name__)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    
    else: 
        with get_db().cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
            g.user = cursor.fetchone()[0]
        


#TODO hacer el registro
@bp.route("/registro", methods = ("GET", "POST"))
def register():
    #cuando se envia el formulario de registro
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        email = request.form["email"]
        password = request.form["password"]
        direccion = request.form["direccion"]
        region = request.form["region"]
        comuna = request.form["comuna"]

        db = get_db()

        try:
            with db.cursor() as cursor:
                
                cursor.execute("SELECT id FROM regiones WHERE nombre = %s", (region,))
                id_region = cursor.fetchone()[0]

                cursor.execute("SELECT id FROM comunas WHERE nombre = %s AND id_region = %s", (comuna, id_region,))         
                id_comuna = cursor.fetchone()[0]

                cursor.execute("""INSERT INTO usuarios (direccion, nombre, apellido, email, password, id_region, id_comuna) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
                               (direccion, 
                                nombre, 
                                apellido, 
                                email, 
                                generate_password_hash(password), 
                                id_region, 
                                id_comuna,)
                            )
                db.commit()

        except IntegrityError as e:
            flash(f"{e}")
        
        except Exception as e:
            flash(f"{e}")

        else:
            return redirect(url_for("login.login"))


    return render_template("registro.html")

@bp.route("/login", methods = ("GET", "POST"))
def login():
    #cuando se envia el formulario de inicio de sesion
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        db = get_db()
        error = None

        with db.cursor() as cursor:

            cursor.execute("SELECT * FROM usuarios where email = %s", (email,))
            user = cursor.fetchone()
        if user is None:
            error = "Correo incorrecto"
        elif not check_password_hash(user["password"], password):
            error = "Contraseña incorrecta"

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))
        flash(error)
    

    return render_template("login.html")

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))