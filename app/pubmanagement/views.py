from flask import render_template, Blueprint, request, jsonify, abort
from flask_login import login_required
import http
from app.login.utils import admin_required
from app import db
from app.models.beer_pub import BeerPub
from app.models.beer_pub_functions import create_beer_pub, delete_beer_pub, get_beer_pub, overlaps_with_any
from app.models.beer_pub_product_functions import get_beer_pub_products,\
													get_beer_pub_product,\
												  	create_beer_pub_product,\
												  	delete_beer_pub_product,\
												  	delete_beer_pub_products
from app.models.product_functions import get_products, get_product
import jsonpickle
from utils.date_utils import to_date

pubmanagement_blueprint = Blueprint('pubmanagement', __name__,
									url_prefix='/pubmanagement',
                                	template_folder="templates",
                                	static_folder="static")

@pubmanagement_blueprint.errorhandler(400)
def api_error(e):
    return jsonify(error=str(e)), 400

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
	startDate = to_date(request.form['startDate'])
	endDate = to_date(request.form['endDate'])
	if overlaps_with_any(startDate, endDate):
		abort(400, "Beer pub overlaps in time with another beer pub")
	
	beerPub = create_beer_pub(startDate, endDate)		
	return jsonify(beerPub.id)

@pubmanagement_blueprint.route('/deletebeerpub', methods=['POST'])
@login_required
@admin_required
def deleteBeerPub():
	beerPub = get_beer_pub(request.form['id'])
	delete_beer_pub_products(beerPub)
	delete_beer_pub(beerPub)
	return ("", http.HTTPStatus.NO_CONTENT)

@pubmanagement_blueprint.route('/editbeerpub', methods=['POST'])
@login_required
@admin_required
def editBeerPub():
	startDate = to_date(request.form['startDate'])
	endDate = to_date(request.form['endDate'])
	if overlaps_with_any(startDate, endDate):
		abort(400, "Beer pub overlaps in time with another beer pub")

	beerPub = get_beer_pub(request.form['id'])
	beerPub.startDate = startDate
	beerPub.endDate = endDate
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
		beerPub=beerPub,
		beerPubProducts=get_beer_pub_products(beerPub),
		get_product=get_product)


@pubmanagement_blueprint.route('/createbeerpubproduct', methods=['POST'])
@login_required
@admin_required
def createBeerPubProduct():
	beerPub = get_beer_pub(request.form['beerPubId'])
	product = get_product(request.form['productId'])
	if get_beer_pub_product(beerPub, product) is not None:
		abort(400, "The beer pub already has the given product in its catalog")
	beerPubProduct = create_beer_pub_product(beerPub, product, request.form['price'])
	return ("", http.HTTPStatus.NO_CONTENT)

@pubmanagement_blueprint.route('/deletebeerpubproduct', methods=['POST'])
@login_required
@admin_required
def deleteBeerPubProduct():
	delete_beer_pub_product(get_beer_pub_product(get_beer_pub(request.form['beerPubId']),
												 get_product(request.form['productId'])))
	return ("", http.HTTPStatus.NO_CONTENT)

@pubmanagement_blueprint.route('/editbeerpubproduct', methods=['POST'])
@login_required
@admin_required
def editBeerPubProduct():
	beerPub = get_beer_pub(request.form['beerPubId'])
	product = get_product(request.form['productId'])
	beerPubProduct = get_beer_pub_product(beerPub, product)
	beerPubProduct.price = request.form['price']
	db.session.commit()
	return ("", http.HTTPStatus.NO_CONTENT)

@pubmanagement_blueprint.route('/possibleproducts/<beerPubId>', methods=['GET'])
@login_required
@admin_required
def possibleProducts(beerPubId):
	beerPub = get_beer_pub(beerPubId)
	possibleProducts = list(set(get_products()) -
		set(map(lambda bpp: get_product(bpp.productId), get_beer_pub_products(beerPub))))
	return jsonify(jsonpickle.encode(possibleProducts, unpicklable=True))