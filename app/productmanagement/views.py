from flask import render_template, Blueprint
from flask_login import login_required
from app.login.utils import admin_required
import http
from app.models.product import Product

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
	return ("", http.HTTPStatus.NO_CONTENT)

@productmanagement_blueprint.route('/delete', methods=['POST'])
@login_required
@admin_required
def delete():
	return ("", http.HTTPStatus.NO_CONTENT)

@productmanagement_blueprint.route('/edit', methods=['POST'])
@login_required
@admin_required
def edit():
	return ("", http.HTTPStatus.NO_CONTENT)