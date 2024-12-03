from flask import Blueprint, render_template, redirect, url_for, request, current_app
from .login import login_required
from flask import g
from .db import get_db
from werkzeug.utils import secure_filename
import os

bp = Blueprint('propietario', __name__, url_prefix='/propietario')

@bp.route('/')
@login_required
def index():
    get_db()
    db = g.get("db")

    with db.cursor() as cursor:
        cursor.execute("select privilegios from usuarios where id = %s", (g.user,))
        privilegios = cursor.fetchone()[0]
        
        if privilegios == 1:
            return render_template("propietario.html")
        else:
            return redirect(url_for("index"))
        
@bp.route('/add_product', methods = ["POST"])
def add():
    if request.method == "POST":
        get_db()
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        precio = request.form["precio"]
        imagen = request.files["imagen"]
        categoria = request.form["categoria"]
        inventario = request.form["inventario"]


        nombre_imagen = secure_filename(imagen.filename)
        filepath = os.path.join(current_app.config['CARPETA_IMAGEN'], nombre_imagen)
        imagen.save(filepath)

        db = g.get("db")

        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO productos (nombre, descripcion, categoria) VALUES (%s, %s, %s) returning id",
                (nombre, descripcion, categoria)
            )
            id_producto = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO formas_producto (id_producto, nombre, precio, inventario, ruta_imagen) VALUES (%s, %s, %s, %s, %s)",
                (id_producto, nombre, precio, inventario, nombre_imagen)
            )

        db.commit()

        return render_template("propietario.html", msg = "producto subido")
            