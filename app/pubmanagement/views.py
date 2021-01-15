from flask import render_template, Blueprint, request, jsonify
from flask_login import login_required
import http
from app.login.utils import admin_required
from app import db
from app.models.beer_pub import create_beer_pub, BeerPub, delete_beer_pub, get_beer_pub
from app.models.beer_pub_product import get_beer_pub_products
from app.models.product import get_products
import jsonpickle

pubmanagement_blueprint = Blueprint('pubmanagement', __name__,
									url_prefix='/pubmanagement',
                                	template_folder="templates",
                                	static_folder="static")

@pubmanagement_blueprint.route('/', methods=['GET'])
@login_required
@admin_required
def home():
	return render_template('pubmanagement.html',
							title="BierKroeg Management",
							columns=["Start", "Einde", "", "Acties"],
							beerPubs=BeerPub.query.all())

@pubmanagement_blueprint.route('/createbeerpub', methods=['POST'])
@login_required
@admin_required
def createBeerPub():
	beerPub = create_beer_pub(request.form['startDate'], request.form['endDate'])
	return jsonify(beerPub.id)

@pubmanagement_blueprint.route('/deletebeerpub', methods=['POST'])
@login_required
@admin_required
def deleteBeerPub():
	delete_beer_pub(request.form['id'])
	return ("", http.HTTPStatus.NO_CONTENT)

@pubmanagement_blueprint.route('/editbeerpub', methods=['POST'])
@login_required
@admin_required
def editBeerPub():
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
	return render_template('catalogus.html',
		title="Catalogus",
		columns=["Product", "Prijs (€)", "Acties"],
		beerPubProducts=get_beer_pub_products(beerPub),
		products=jsonpickle.encode(get_products(), unpicklable=False))


@pubmanagement_blueprint.route('/createbeerpubproduct', methods=['POST'])
@login_required
@admin_required
def createBeerPubProduct():
	return ("", http.HTTPStatus.NO_CONTENT)

@pubmanagement_blueprint.route('/deletebeerpubproduct', methods=['POST'])
@login_required
@admin_required
def deleteBeerPubProduct():
	return ("", http.HTTPStatus.NO_CONTENT)

@pubmanagement_blueprint.route('/editbeerpubproduct', methods=['POST'])
@login_required
@admin_required
def editBeerPubProduct():
	return ("", http.HTTPStatus.NO_CONTENT)