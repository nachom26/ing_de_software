from flask import Blueprint
from flask import render_template
from flask import g

bp = Blueprint("tienda", __name__)

@bp.route("/")
def index():
    return render_template("index.html", data = g.user)