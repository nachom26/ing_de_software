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
        cursor.execute("select productos.id, productos.nombre, formas_producto.precio, formas_producto.ruta_imagen from productos join formas_producto on productos.id = formas_producto.id_producto left join valoraciones on productos.id = valoraciones.id_producto")
        productos = cursor.fetchall()
        current_app.logger.info(productos)
    return render_template("index.html", user = user, productos = productos)