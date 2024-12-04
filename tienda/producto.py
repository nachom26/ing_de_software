from flask import Blueprint, render_template, g, current_app
from .db import get_db

bp = Blueprint("producto", __name__, url_prefix="/producto")

@bp.route("/<int:producto_id>")
def producto(producto_id):
    get_db()
    db = g.get("db")
    with db.cursor() as cursor:
        cursor.execute("select formas_producto.id, formas_producto.nombre, precio, inventario, ruta_imagen, medidas, color, productos.descripcion from formas_producto join productos on productos.id = id_producto where id_producto = %s", (producto_id,))
        productos = cursor.fetchone()

    return render_template("producto.html", productos = productos)