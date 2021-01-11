from flask import render_template, Blueprint, make_response, request, jsonify
from flask_login import login_required
from app.login.utils import admin_required
from app.models.beer_pub import create_beer_pub, BeerPub, delete_beer_pub
import http

pubmanagement_blueprint = Blueprint('pubmanagement', __name__,
									url_prefix='/pubmanagement',
                                	template_folder="templates",
                                	static_folder="static")

@pubmanagement_blueprint.route('/', methods=['GET'])
@login_required
@admin_required
def home():
	return make_response(render_template('pubmanagement.html', beerPubs=BeerPub.query.all()))

@pubmanagement_blueprint.route('/create', methods=['POST'])
@login_required
@admin_required
def create():
	beerPub = create_beer_pub(request.form['startDate'], request.form['endDate'])
	return jsonify(beerPub.id)

@pubmanagement_blueprint.route('/delete', methods=['POST'])
@login_required
@admin_required
def delete():
	delete_beer_pub(request.form['id'])
	return ("", http.HTTPStatus.NO_CONTENT)