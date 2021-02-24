from flask import render_template, Blueprint
from flask_login import login_required
from app.common.loginutils import admin_required
from app.models.product.product import Product
from ..blueprint import productmanagement_blueprint

@productmanagement_blueprint.route('/', methods=['GET'])
@login_required
@admin_required
def home():
    return render_template('productmanagement.html',
                            title="Product Management",
                            columns=["Naam", "Acties"],
                            products=Product.query.all())