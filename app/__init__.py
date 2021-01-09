import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from .config import BaseConfig

# instantiate the extensions
bootstrap = Bootstrap()
db = SQLAlchemy()

dbModel = None

def createDb():
    from .login.models import User
    from .models.beer_pub import BeerPub
    from .models.price import Price
    from .models.product import Product
    db.create_all()

def create_app():
    global dbModel

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
    
    app.secret_key = app.config['SECRET_KEY']
    
    # set up extensions
    bootstrap.init_app(app)
    db.init_app(app)
    with app.app_context():
        dbModel = automap_base()
        schema = app.config['DB_SCHEMA']
        dbModel.prepare(db.engine, reflect=True, schema=app.config['DB_SCHEMA'])
        from .login import create_admin, login
        login.init_app(app)
        createDb()
        create_admin()

    # register blueprints
    from .main.views import main_blueprint
    app.register_blueprint(main_blueprint)
    from .login.views import login_blueprint
    app.register_blueprint(login_blueprint)
    from .pubmanagement.views import pubmanagement_blueprint
    app.register_blueprint(pubmanagement_blueprint)
    from .waiter.views import waiter_blueprint
    app.register_blueprint(waiter_blueprint)

    # shell context for flask cli
    app.shell_context_processor({'app': app})
    return app