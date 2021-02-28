import os
from flask import Flask, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from .config import BaseConfig

# instantiate the extensions
bootstrap = Bootstrap()
db = SQLAlchemy()

dbModel = None

def createDb():
    from .models.user.user import User
    from .models.user.role import Role
    from .models.user.userrole import UserRole
    from .models.beer_pub import BeerPub
    from .models.product.beer_pub_product import BeerPubProduct
    from .models.product.product import Product
    from .models.order.order import Order
    from .models.order.event import Event
    from .models.order.orderevent import OrderEvent
    from .models.order.orderproduct import OrderProduct
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
        from .models.user.role import Role
        from .models.order.event import Event
        login.init_app(app)
        createDb()
        Role.create_roles()
        create_admin()
        Event.create_events()

        from .handlers.errorhandlers import api_error, no_active_beer_pub

        @app.route('/')
        def home():
            return redirect(url_for("home.home"), code=302)

    # register blueprints
    from .home.blueprint import home_blueprint
    app.register_blueprint(home_blueprint)
    from .login.blueprint import login_blueprint
    app.register_blueprint(login_blueprint)
    from .pubmanagement.blueprint import pubmanagement_blueprint
    app.register_blueprint(pubmanagement_blueprint)
    from .productmanagement.blueprint import productmanagement_blueprint
    app.register_blueprint(productmanagement_blueprint)
    from .order.blueprint import order_blueprint
    app.register_blueprint(order_blueprint)
    from .usermanagement.blueprint import usermanagement_blueprint
    app.register_blueprint(usermanagement_blueprint)


    # shell context for flask cli
    app.shell_context_processor({'app': app})
    return app