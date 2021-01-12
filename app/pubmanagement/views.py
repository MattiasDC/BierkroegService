from flask import render_template, Blueprint, make_response, request, jsonify
from flask_login import login_required
from app.login.utils import admin_required
from app import db
from app.models.beer_pub import create_beer_pub, BeerPub, delete_beer_pub, get_beer_pub
import http
from app.models.beer_pub_product import get_beer_pub_products

pubmanagement_blueprint = Blueprint('pubmanagement', __name__,
									url_prefix='/pubmanagement',
                                	template_folder="templates",
                                	static_folder="static")

@pubmanagement_blueprint.route('/', methods=['GET'])
@login_required
@admin_required
def home():
	return render_template('pubmanagement.html', beerPubs=BeerPub.query.all())

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

@pubmanagement_blueprint.route('/edit', methods=['POST'])
@login_required
@admin_required
def edit():
	beerPub = get_beer_pub(request.form['id'])
	beerPub.startDate = request.form['startDate']
	beerPub.endDate = request.form['endDate']
	db.session.commit()
	return ("", http.HTTPStatus.NO_CONTENT)

@pubmanagement_blueprint.route('/catalogus/<id>', methods=['GET'])
@login_required
@admin_required
def catalogus(id):
	beerPub = get_beer_pub(id)
	return render_template('catalogus.html', beerPub=beerPub, beerPubProducts=get_beer_pub_products(beerPub))