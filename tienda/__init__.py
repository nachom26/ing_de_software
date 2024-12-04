import os

from flask import Flask



def create_app(test_config = None):

    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE_URL="postgresql://tienda:2643@191.112.190.249:5432/tienda"
    )

    CARPETA_IMAGEN = 'D:/Nakzit/Documentos2/Universidad/ing_de_software/tienda/static/imgs'
    app.config['CARPETA_IMAGEN'] = CARPETA_IMAGEN

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
    from . import carrito
    from . import propietario
    from . import configuracion
    from . import producto

    app.register_blueprint(login.bp)
    app.register_blueprint(index.bp)
    app.register_blueprint(carrito.bp)
    app.register_blueprint(propietario.bp)
    app.register_blueprint(configuracion.bp)
    app.register_blueprint(producto.bp)

    app.add_url_rule("/", endpoint="index")

    return app