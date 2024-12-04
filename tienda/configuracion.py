from flask import Blueprint, request, render_template, g, current_app
from werkzeug.security import generate_password_hash
import logging
from .login import login_required
from .db import get_db

bp = Blueprint('configuracion', __name__, url_prefix='/conf')

@bp.route('/', methods=['GET', 'POST'])
@login_required
def conf():
    get_db()
    db = g.get("db")
    with db.cursor() as cursor:
        cursor.execute("""SELECT usuarios.nombre, apellido, email, direccion, regiones.nombre, comunas.nombre 
                          FROM usuarios 
                          JOIN regiones ON regiones.id = usuarios.id_region 
                          JOIN comunas ON comunas.id = usuarios.id_comuna 
                          WHERE usuarios.id = %s""",
                       (g.user,))
        user = cursor.fetchone()

    # Al enviarse un form
    if request.method == 'POST':
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        email = request.form["email"]
        direccion = request.form["direccion"]
        region = request.form["region"]
        comuna = request.form["comuna"]
        password = request.form["password"]

        # Convertir los nombres de región y comuna a sus respectivos IDs
        id_region = None
        id_comuna = None

        current_app.logger.info(region)

        if region:
            with db.cursor() as cursor:
                cursor.execute("SELECT id FROM regiones WHERE nombre = %s", (region,))
                id_region = cursor.fetchone()[0]
        if comuna:
            with db.cursor() as cursor:
                cursor.execute("SELECT id FROM comunas WHERE nombre = %s", (comuna,))
                id_comuna = cursor.fetchone()[0]

        new_data = {
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'direccion': direccion,
            'id_region': id_region,
            'id_comuna': id_comuna
        }

        update_fields = []
        update_values = []

        for i, (field, new_value) in enumerate(new_data.items()):
            if new_value and new_value != user[i]:
                update_fields.append(f"{field} = %s")
                update_values.append(new_value)

        if update_fields:
            update_values.append(g.user)  # Añade el ID del usuario para la cláusula WHERE
            update_query = f"UPDATE usuarios SET {', '.join(update_fields)} WHERE id = %s"

            with db.cursor() as cursor:
                cursor.execute(update_query, update_values)
                db.commit()

        if password:
            cursor.execute("update usuarios set password = %s where id = %s", (generate_password_hash(password), g.user))


        # Volver a obtener los datos del usuario actualizados
        with db.cursor() as cursor:
            cursor.execute("""SELECT usuarios.nombre, apellido, email, direccion, regiones.nombre, comunas.nombre 
                                FROM usuarios 
                                JOIN regiones ON regiones.id = usuarios.id_region 
                                JOIN comunas ON comunas.id = usuarios.id_comuna 
                                WHERE usuarios.id = %s""",
                            (g.user,))
            user = cursor.fetchone()
            

        return render_template("configuracion.html", user=user, msg="Datos actualizados")

    return render_template("configuracion.html", user=user)