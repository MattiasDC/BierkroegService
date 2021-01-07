from flask import render_template, Blueprint, make_response
from app import dbModel, db
from flask_login import login_required

waiter_blueprint = Blueprint('waiter', __name__,
								url_prefix='/waiter',
                                template_folder="templates",
                                static_folder="static")

@waiter_blueprint.route('/', methods=['GET'])
@login_required
def home():
	Product = dbModel.classes.Product
	products = db.session.query(Product).all()
	return make_response(render_template('waiter.html', products=products))