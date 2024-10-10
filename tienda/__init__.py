import os

from flask import Flask


def create_app():

    app = Flask(__name__)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route('/test')
    def test():
        return 'Hello World!'
    
    from . import db

    #db.init(app)

    from . import login
    from . import index

    app.register_blueprint(login.bp)
    app.register_blueprint(index.bp)

    app.add_url_rule("/", endpoint="index")

    return app