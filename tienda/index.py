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
    current_app.logger.info(user)
    return render_template("index.html", data = user)