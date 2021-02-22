from flask import render_template, Blueprint, request, abort, jsonify, current_app as app
from flask_login import login_required, current_user
from app.login.utils import roles_required
from app.models.user.role import Role
from app.models.beer_pub import BeerPub
from app.models.order.order import Order
from app.models.product.product import Product
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
@roles_required(Role.get_waiter_id())
def waiter():
    return render_template('order.html',
        beer_pub=BeerPub.get_active(),
        waiter=True)

@order_blueprint.route('/cashdeskorder', methods=['GET'])
@login_required
@roles_required(Role.get_cash_desk_id())
def cash_desk_order():
    return render_template('order.html',
        beer_pub=BeerPub.get_active(),
        cash_desk=True)

def get_ordered_time_formatted(datetime):
    if datetime.date() == date.today():
        return datetime.time().isoformat('minutes')
    return datetime.isoformat(' ', 'minutes')

def get_sorted_orders(orders):
    return sorted(orders, key=lambda order: (get_event_logical_ordering(order.get_last_event()), -get_ordered_time_formatted(order.get_ordered_time()).timestamp()))

@order_blueprint.route('/orderhistory', methods=['GET'])
@login_required
@roles_required(Role.get_cash_desk_id())
def order_history():
    return render_template('orderhistory.html',
        title="Bestellingen",
        columns=["", "Id", "Persoon", "Bedrag", "Status", "Besteld", "Opmerkingen", "Acties"],
        beer_pub=BeerPub.get_active(),
        get_ordered_time_formatted=get_ordered_time_formatted)

def new_order(user, paidAtOrder):
    beerPub = BeerPub.get_active()
    if beerPub is None:
        abort(400, "There is no active beer pub!")

    table = request.form['table']
    products = request.form.getlist('products[]')
    amounts = request.form.getlist('amounts[]')
    remarks = request.form['remarks']
    Order.create(beerPub, user, list(map(Product.get, products)), amounts, table, paidAtOrder, remarks)
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
def deleteOrder():
    order = Order.get(request.form['id'])
    if order is not None:
        order.delete()
    return ("", http.HTTPStatus.NO_CONTENT)