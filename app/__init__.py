import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from app.config import BaseConfig

# instantiate the extensions
bootstrap = Bootstrap()
db = SQLAlchemy()

dbModel = None

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
        dbModel.prepare(db.engine, reflect=True, schema=app.config['DB_SCHEMA'])

    # register blueprints
    from app.main.views import main_blueprint
    app.register_blueprint(main_blueprint)
    from app.waiter.views import waiter_blueprint
    app.register_blueprint(waiter_blueprint)

    # shell context for flask cli
    app.shell_context_processor({'app': app})
    return app