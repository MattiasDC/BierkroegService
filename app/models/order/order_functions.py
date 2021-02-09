from app import db
from .order import Order
from .event import get_ordered_event, get_ordered_event_id
from .orderevent import create_order_event, OrderEvent, delete_order_events
from .orderproduct import create_order_products, delete_order_products

def get_orders(beerPub):
	if beerPub is None:
		return []
	return Order.query.filter_by(beerPubId=beerPub.id)

def get_order(orderId):
	return Order.query.filter_by(id=orderId).one_or_none()

def create_order(beerPub, waiter, products, amounts, table, paidAtOrder):
	order = Order(beerPubId=beerPub.id, waiter=waiter.username, paidAtOrder=paidAtOrder, table=table)
	db.session.add(order)
	db.session.commit()

	event = get_ordered_event()
	create_order_event(order, event)
	create_order_products(order, products, amounts)

def delete_order(order):
	delete_order_events(order)
	delete_order_products(order)
	db.session.delete(order)
	db.session.commit()

