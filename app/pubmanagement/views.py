from flask import render_template, Blueprint, make_response
from app import dbModel, db
from flask_login import login_required
from app.login.utils import admin_required
from app.models.beer_pub import BeerPub

pubmanagement_blueprint = Blueprint('pubmanagement', __name__,
									url_prefix='/pubmanagement',
                                	template_folder="templates",
                                	static_folder="static")

@pubmanagement_blueprint.route('/', methods=['GET'])
@login_required
@admin_required
def home():
	return make_response(render_template('pubmanagement.html', beerPubs=BeerPub.query.all()))