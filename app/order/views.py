from flask import render_template, Blueprint, request, abort, jsonify, current_app as app
from flask_login import login_required, current_user
from app.models.product.beer_pub_product_functions import get_beer_pub_products
from app.models.product.product_functions import get_product
from app.models.beer_pub_functions import get_active_beer_pub
from app.models.order.order_functions import get_orders, create_order
from app.login.utils import roles_required
from app.models.user.role import get_waiter_id, get_cash_desk_id
import http

order_blueprint = Blueprint('order', __name__,
							 url_prefix='/order',
                             template_folder="templates",
                             static_folder="static")

@order_blueprint.errorhandler(400)
def api_error(e):
    return jsonify(error=str(e)), 400

@order_blueprint.route('/waiter', methods=['GET'])
@login_required
@roles_required(get_waiter_id())
def waiter():
	beerPub = get_active_beer_pub()
	return render_template('order.html',
		products=get_beer_pub_products(beerPub),
		beerPub=beerPub,
		get_product=get_product,
		waiter=True)

@order_blueprint.route('/cashdeskorder', methods=['GET'])
@login_required
@roles_required(get_cash_desk_id())
def cash_desk_order():
	beerPub = get_active_beer_pub()
	return render_template('order.html',
		products=get_beer_pub_products(beerPub),
		beerPub=beerPub,
		get_product=get_product,
		cash_desk=True)

@order_blueprint.route('/orderhistory', methods=['GET'])
@login_required
@roles_required(get_cash_desk_id())
def order_history():
	return render_template('orderhistory.html',
		title="Bestellingen",
		columns=["Id"],
		orders=get_orders(get_active_beer_pub()))

@order_blueprint.route('/newwaiterorder', methods=['POST'])
@login_required
@roles_required(get_waiter_id())
def new_waiter_order():
	beerPub = get_active_beer_pub()
	if beerPub is None:
		abort(400, "There is no active beer pub!")

	waiter = current_user.user
	table = request.form['table']
	products = request.form.getlist('products[]')
	amounts = request.form.getlist('amounts[]')
	create_order(beerPub, waiter, list(map(get_product, products)), amounts, table, True)
	return ("", http.HTTPStatus.NO_CONTENT)