from flask import render_template, Blueprint, current_app as app
from flask_login import login_required, current_user
from app.common.get_active_beer_pub import get_active_beer_pub
from app.common.loginutils import roles_required
from app.models.user.role import Role
from ..blueprint import order_blueprint
import http
from datetime import date

@order_blueprint.route('/waiter', methods=['GET'])
@login_required
@roles_required(Role.get_waiter_id())
def waiter():
    return render_template('order.html',
        beer_pub=get_active_beer_pub(),
        waiter=True)

@order_blueprint.route('/cashdeskorder', methods=['GET'])
@login_required
@roles_required(Role.get_cash_desk_id())
def cash_desk_order():
    return render_template('order.html',
        beer_pub=get_active_beer_pub(),
        cash_desk=True)

def get_ordered_time_formatted(datetime):
    if datetime.date() == date.today():
        return datetime.time().isoformat('minutes')
    return datetime.isoformat(' ', 'minutes')

def get_sorted_orders(orders):
    return sorted(orders, key=lambda order: (order.get_last_event(), -order.get_ordered_time().timestamp()))

@order_blueprint.route('/orderhistory', methods=['GET'])
@login_required
@roles_required(Role.get_cash_desk_id())
def order_history():
    return render_template('orderhistory.html',
        title="Bestellingen",
        columns=["", "Id", "Persoon", "Bedrag", "Status", "Besteld", "Opmerkingen", "Acties"],
        beer_pub=get_active_beer_pub(),
        get_sorted_orders=get_sorted_orders,
        get_ordered_time_formatted=get_ordered_time_formatted)