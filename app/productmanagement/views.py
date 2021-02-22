from flask import render_template, Blueprint, request, jsonify, abort
from flask_login import login_required
from app.login.utils import admin_required
from app import db
import http
from app.models.product.product import Product
from app.models.beer_pub import BeerPub
import jsonpickle

productmanagement_blueprint = Blueprint('productmanagement', __name__,
                                        url_prefix='/productmanagement',
                                        template_folder="templates",
                                        static_folder="static")

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
    if Product.exist(name):
        abort(400, "A product with the same name already exists")
    product = Product.create(name)
    db.session.commit()
    return jsonify(product.id)

@productmanagement_blueprint.route('/delete', methods=['POST'])
@login_required
@admin_required
def delete():
    product = Product.get(request.form['id'])
    if product is None:
        return ("", http.HTTPStatus.NO_CONTENT)    
    if len(BeerPub.get_from_product(product)) != 0:
        abort(400, description="Cannot remove a product which is being used in a beer pub.") 
    product.delete()
    db.session.commit()
    return ("", http.HTTPStatus.NO_CONTENT)


@productmanagement_blueprint.route('/edit', methods=['POST'])
@login_required
@admin_required
def edit():
    name = request.form['name']
    product = Product.get(request.form['id'])
    if not product.can_change_name(name):
        abort(400, "A product with the same name already exists")
    
    product.name = request.form['name']
    db.session.commit()
    return ("", http.HTTPStatus.NO_CONTENT)

@productmanagement_blueprint.route('/products', methods=['GET'])
@login_required
@admin_required
def products():
    return jsonify(jsonpickle.encode(Product.get_all(), unpicklable=True))