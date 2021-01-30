from flask import render_template, Blueprint, current_app as app
from flask_login import login_required
from app.models.product.beer_pub_product_functions import get_beer_pub_products
from app.models.product.product_functions import get_product
from app.models.beer_pub_functions import get_active_beer_pub
from app.login.utils import roles_required
from app.models.user.role import get_waiter_id, get_cash_desk_id

order_blueprint = Blueprint('order', __name__,
							 url_prefix='/order',
                             template_folder="templates",
                             static_folder="static")

@order_blueprint.route('/waiter', methods=['GET'])
@login_required
@roles_required(get_waiter_id())
def waiter():
	return render_template('order.html',
		products=get_beer_pub_products(get_active_beer_pub()),
		get_product=get_product,
		waiter=True)

@order_blueprint.route('/cashdesk', methods=['GET'])
@login_required
@roles_required(get_cash_desk_id())
def cash_desk():
	return render_template('order.html',
		products=get_beer_pub_products(get_active_beer_pub()),
		get_product=get_product,
		cash_desk=True)