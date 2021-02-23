from flask import render_template, Blueprint, request, jsonify, abort
from flask_login import login_required
import http
from app.common.loginutils import admin_required
from app.models.beer_pub import BeerPub
from app.models.product.product import Product
import jsonpickle
from utils.date_utils import to_date
from app import db
from ..blueprint import pubmanagement_blueprint

@pubmanagement_blueprint.route('/', methods=['GET'])
@login_required
@admin_required
def home():
    return render_template('pubmanagement.html',
                            title="BierKroeg Management",
                            columns=["Start", "Einde", "Catalogus", "Acties"],
                            beer_pubs=BeerPub.get_all())

@pubmanagement_blueprint.route('/createbeerpub', methods=['POST'])
@login_required
@admin_required
def create_beer_pub():
    start_date = to_date(request.form['startDate'])
    end_date = to_date(request.form['endDate'])
    if end_date < start_date:
        abort(400, "Start date cannot be before end date!")

    beer_pub = BeerPub.create(start_date, end_date)
    if beer_pub is None:
        abort(400, "Beer pub overlaps in time with another beer pub")
    db.session.commit()
    return jsonify(beer_pub.id)

@pubmanagement_blueprint.route('/deletebeerpub', methods=['POST'])
@login_required
@admin_required
def delete_beer_pub():
    beer_pub = BeerPub.get(request.form['id'])
    if beer_pub is None:
        return ("", http.HTTPStatus.NO_CONTENT)

    if len(beer_pub.get_orders()) > 0:
        abort(400, "A beer pub with orders cannot be deleted")
    beer_pub.delete()
    db.session.commit()
    return ("", http.HTTPStatus.NO_CONTENT)

@pubmanagement_blueprint.route('/editbeerpub', methods=['POST'])
@login_required
@admin_required
def edit_beer_pub():
    start_date = to_date(request.form['startDate'])
    end_date = to_date(request.form['endDate'])
    if end_date < start_date:
        abort(400, "Start date cannot be before end date!")

    beer_pub = BeerPub.get(request.form['id'])
    beer_pub.start_date = start_date
    beer_pub.end_date = end_date
    db.session.commit()
    return ("", http.HTTPStatus.NO_CONTENT)

@pubmanagement_blueprint.route('/catalogus/<id>', methods=['GET'])
@login_required
@admin_required
def catalogus(id):
    beer_pub = BeerPub.get(id)
    return render_template('catalogus.html',
        title="Catalogus",
        columns=["Product", "Prijs (€)", "Acties"],
        beer_pub=beer_pub)


@pubmanagement_blueprint.route('/addproduct', methods=['POST'])
@login_required
@admin_required
def add_product():
    beer_pub = BeerPub.get(request.form['beerPubId'])
    product = Product.get(request.form['productId'])
    beer_pub.add_product(product, float(request.form['price']))
    db.session.commit()
    return ("", http.HTTPStatus.NO_CONTENT)

@pubmanagement_blueprint.route('/removeproduct', methods=['POST'])
@login_required
@admin_required
def remove_product():
    product = Product.get(request.form['productId'])
    if product is not None:
        BeerPub.get(request.form['beerPubId']).remove_product(product)
        db.session.commit()
    return ("", http.HTTPStatus.NO_CONTENT)

@pubmanagement_blueprint.route('/editproduct', methods=['POST'])
@login_required
@admin_required
def edit_product():
    beer_pub = BeerPub.get(request.form['beerPubId'])
    product = Product.get(request.form['productId'])
    beer_pub.change_price(product, float(request.form['price']))
    db.session.commit()
    return ("", http.HTTPStatus.NO_CONTENT)

@pubmanagement_blueprint.route('/possibleproducts/<beerPubId>', methods=['GET'])
@login_required
@admin_required
def possible_products(beerPubId):
    beer_pub = BeerPub.get(beerPubId)
    possible_products = list(set(Product.get_all()) - set(beer_pub.get_products()))
    return jsonify(jsonpickle.encode(possible_products, unpicklable=True))