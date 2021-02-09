from flask import render_template, Blueprint, request, abort, jsonify, current_app as app
from flask_login import login_required, current_user
from app.models.product.beer_pub_product_functions import get_beer_pub_products
from app.models.product.product_functions import get_product
from app.models.beer_pub_functions import get_active_beer_pub
from app.models.order.order_functions import get_orders, create_order, get_order, delete_order
from app.models.order.orderevent import get_last_event, get_creation_time
from app.models.order.orderproduct import get_order_total_price
from app.models.order.event import translate_event, get_event_logical_ordering
from app.login.utils import roles_required
from app.models.user.role import get_waiter_id, get_cash_desk_id
import http
from datetime import date

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

def get_order_creation_time(order):
    creationTime = get_creation_time(order)
    if creationTime.date() == date.today():
        return creationTime.time().isoformat('minutes')
    return creationTime.isoformat(' ', 'minutes')

def get_sorted_orders(orders):
    return sorted(orders, key=lambda order: (get_event_logical_ordering(get_last_event(order)), -get_creation_time(order).timestamp()))

@order_blueprint.route('/orderhistory', methods=['GET'])
@login_required
@roles_required(get_cash_desk_id())
def order_history():
    return render_template('orderhistory.html',
        title="Bestellingen",
        columns=["Id", "Persoon", "Bedrag", "Status", "Besteld", "Acties"],
        orders=get_sorted_orders(get_orders(get_active_beer_pub())),
        get_last_event=lambda order: translate_event(get_last_event(order).eventId).capitalize(),
        get_creation_time=get_order_creation_time,
        get_order_total_price=get_order_total_price)

def new_order(user, paidAtOrder):
    beerPub = get_active_beer_pub()
    if beerPub is None:
        abort(400, "There is no active beer pub!")

    table = request.form['table']
    products = request.form.getlist('products[]')
    amounts = request.form.getlist('amounts[]')
    create_order(beerPub, user, list(map(get_product, products)), amounts, table, paidAtOrder)
    return ("", http.HTTPStatus.NO_CONTENT)

@order_blueprint.route('/newwaiterorder', methods=['POST'])
@login_required
@roles_required(get_waiter_id())
def new_waiter_order():
    waiter = current_user.user
    return new_order(waiter, True)

@order_blueprint.route('/newcashdeskorder', methods=['POST'])
@login_required
@roles_required(get_cash_desk_id())
def new_cash_desk_order():
    cash_desk_user = current_user.user
    return new_order(cash_desk_user, False)

@order_blueprint.route('/deleteorder', methods=['POST'])
@login_required
@roles_required(get_cash_desk_id())
def deleteOrder():
    orderId = request.form['id']
    order = get_order(orderId)
    if order is not None:
        delete_order(order)
    return ("", http.HTTPStatus.NO_CONTENT)