from flask import render_template, Blueprint, request, jsonify
from flask_login import login_required
from app.login.utils import admin_required
from app import db
import http
from app.models.product import Product, create_product, delete_product, get_product

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
	product = create_product(request.form['name'])
	return jsonify(product.id)

@productmanagement_blueprint.route('/delete', methods=['POST'])
@login_required
@admin_required
def delete():
	delete_product(request.form['id'])
	return ("", http.HTTPStatus.NO_CONTENT)

@productmanagement_blueprint.route('/edit', methods=['POST'])
@login_required
@admin_required
def edit():
	product = get_product(request.form['id'])
	product.name = request.form['name']
	db.session.commit()
	return ("", http.HTTPStatus.NO_CONTENT)