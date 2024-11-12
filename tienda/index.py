from flask import Blueprint
from flask import render_template
from flask import g
from flask import current_app
from .db import get_db

bp = Blueprint("tienda", __name__)

@bp.route("/")
def index():

    get_db()
    db = g.get("db")
    with db.cursor() as cursor:
        cursor.execute("select nombre, apellido from usuarios where id = %s", (g.user,))
        user= cursor.fetchone()
    with db.cursor() as cursor:
        cursor.execute("select * from productos join formas_producto on productos.id = formas_producto.id_producto join valoraciones on productos.id = valoraciones.id_producto")
        productos = cursor.fetchall()
    return render_template("index.html", user = user, productos = productos)