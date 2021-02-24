from flask import Blueprint, request, jsonify, abort
from flask_login import login_required
import http
from app.common.loginutils import admin_required
from app.models.beer_pub import BeerPub
from app.models.product.product import Product
import jsonpickle
from utils.date_utils import to_date
from app import db
from .blueprint import pubmanagement_blueprint

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

    if len(beer_pub.orders) > 0:
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
    if beer_pub is None:
        abort(400, "An invalid beer pub was given!")
        
    if len(beer_pub.orders) > 0:
        abort(400, "A beer pub with orders cannot have it's date changed!")

    beer_pub.start_date = start_date
    beer_pub.end_date = end_date

    if beer_pub.overlaps_with_any():
        db.session.rollback()
        abort(400, "Beer pub cannot overlap with another beer pub")
    else:
        db.session.commit()
    return ("", http.HTTPStatus.NO_CONTENT)

@pubmanagement_blueprint.route('/addproduct', methods=['POST'])
@login_required
@admin_required
def add_product():
    beer_pub = BeerPub.get(request.form['beerPubId'])
    product = Product.get(request.form['productId'])

    if not beer_pub.has_product(product):
        beer_pub.add_product(product, float(request.form['price']))
        db.session.commit()
    return ("", http.HTTPStatus.NO_CONTENT)

@pubmanagement_blueprint.route('/removeproduct', methods=['POST'])
@login_required
@admin_required
def remove_product():
    product = Product.get(request.form['productId'])
    beer_pub = BeerPub.get(request.form['beerPubId'])
    if product is not None and beer_pub is not None and beer_pub.has_product(product):
        beer_pub.remove_product(product)
        db.session.commit()
    return ("", http.HTTPStatus.NO_CONTENT)

@pubmanagement_blueprint.route('/editproduct', methods=['POST'])
@login_required
@admin_required
def edit_product():
    beer_pub = BeerPub.get(request.form['beerPubId'])
    product = Product.get(request.form['productId'])
    if beer_pub is not None and product is not None:
        beer_pub.change_price(product, float(request.form['price']))
        db.session.commit()
    return ("", http.HTTPStatus.NO_CONTENT)

@pubmanagement_blueprint.route('/possibleproducts/<beer_pub_id>', methods=['GET'])
@login_required
@admin_required
def possible_products(beer_pub_id):
    beer_pub = BeerPub.get(beer_pub_id)
    possible_products = Product.get_all()
    if beer_pub is not None:
        possible_products = list(possible_products - set(beer_pub.get_products()))
    return jsonify(jsonpickle.encode(possible_products, unpicklable=True))