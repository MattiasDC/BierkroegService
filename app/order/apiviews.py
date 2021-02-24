from flask import Blueprint, request, abort, current_app as app
from flask_login import login_required, current_user
from app.common.get_active_beer_pub import get_active_beer_pub
from app.common.loginutils import roles_required
from app.models.user.role import Role
from app.models.order.order import Order
from app.models.product.product import Product
from utils.isfloat import is_float
from .blueprint import order_blueprint
import http
from app import db

def new_order(user, paid_at_order):
    beerPub = get_active_beer_pub()

    table = request.form['table']
    products = list(map(Product.get, request.form.getlist('products[]')))
    if any((p is None for p in products)):
    	abort(400, "Some passed products are invalid!")

    amounts = request.form.getlist('amounts[]')
    if any((not is_float(a) for a in amounts)):
    	abort(400, "Some passed amounts are invalid!")

    remarks = request.form['remarks']
    Order.create(beerPub, user, products, list(map(float, amounts)), table, paid_at_order, remarks)
    db.session.commit()
    return ("", http.HTTPStatus.NO_CONTENT)

@order_blueprint.route('/newwaiterorder', methods=['POST'])
@login_required
@roles_required(Role.get_waiter_id())
def new_waiter_order():
    return new_order(current_user.user, True)

@order_blueprint.route('/newcashdeskorder', methods=['POST'])
@login_required
@roles_required(Role.get_cash_desk_id())
def new_cash_desk_order():
    return new_order(current_user.user, False)

@order_blueprint.route('/deleteorder', methods=['POST'])
@login_required
@roles_required(Role.get_cash_desk_id())
def delete_order():
    order = Order.get(request.form['id'])
    if order is not None:
        order.delete()
        db.session.commit()
    return ("", http.HTTPStatus.NO_CONTENT)