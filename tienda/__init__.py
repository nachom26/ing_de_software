import os

from flask import Flask



def create_app(test_config = None):

    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",
        #TODO crear bdd y agregar url
        DATABASE_URL="postgresql://tienda:2643@localhost:5432/tienda"
    )
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)


    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db

    db.init_app(app)

    from . import login
    from . import index

    app.register_blueprint(login.bp)
    app.register_blueprint(index.bp)

    app.add_url_rule("/", endpoint="index")

    return app