import psycopg2
from psycopg2.extras import DictCursor
from flask import current_app, g
import click
import logging


def get_db():
    if "db" not in g:
        try:
            g.db = psycopg2.connect(current_app.config["DATABASE_URL"],
                                    cursor_factory=DictCursor)
            g.db.set_client_encoding('UTF8')
            
        except psycopg2.DatabaseError as e:
            current_app.logger.info(f"Error al conectar a la base de datos: {e}")
            return None

        return g.db


def close_db(e=None):

    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_db():
    db=get_db()
    with current_app.open_resource("schema.sql") as f:
        with db.cursor() as cursor:
            cursor.execute(f.read().decode("utf8"))
        db.commit()

@click.command("init_db")
def init_db_command():
    init_db()
    click.echo("Base de datos inicializada")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)