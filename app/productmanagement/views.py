from flask import render_template, Blueprint, request, jsonify, abort
from flask_login import login_required
from app.login.utils import admin_required
from app import db
import http
from app.models.product.product import Product
from app.models.product.product_functions import create_product,\
                                                 delete_product,\
                                                 get_product,\
                                                 get_products,\
                                                 can_delete_product,\
                                                 has_product_with_name

import jsonpickle

productmanagement_blueprint = Blueprint('productmanagement', __name__,
                                        url_prefix='/productmanagement',
                                        template_folder="templates",
                                        static_folder="static")

@productmanagement_blueprint.errorhandler(400)
def api_error(e):
    return jsonify(error=str(e)), 400

@productmanagement_blueprint.route('/', methods=['GET'])
@login_required
@admin_required
def home():
    return render_template('productmanagement.html',
                            title="Product Management",
                            columns=["Naam", "Acties"],
                            products=Product.query.all())

@productmanagement_blueprint.route('/create', methods=['POST'])
@login_required
@admin_required
def create():
    name = request.form['name']
    if has_product_with_name(name, None):
        abort(400, "A product with the same name already exists")
    product = create_product(name)
    return jsonify(product.id)

@productmanagement_blueprint.route('/delete', methods=['POST'])
@login_required
@admin_required
def delete():
    product = get_product(request.form['id'])
    if not can_delete_product(product):
        abort(400, description="Cannot remove a product which is being used in a beer pub.") 
    delete_product(product)
    return ("", http.HTTPStatus.NO_CONTENT)


@productmanagement_blueprint.route('/edit', methods=['POST'])
@login_required
@admin_required
def edit():
    name = request.form['name']
    product = get_product(request.form['id'])
    if has_product_with_name(name, product):
        abort(400, "A product with the same name already exists")
    
    product.name = request.form['name']
    db.session.commit()
    return ("", http.HTTPStatus.NO_CONTENT)

@productmanagement_blueprint.route('/products', methods=['GET'])
@login_required
@admin_required
def products():
    return jsonify(jsonpickle.encode(get_products(), unpicklable=True))