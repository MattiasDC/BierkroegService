from app import db
from .order import Order
from .event import get_ordered_event
from .orderevent import create_order_event
from .orderproduct import create_order_products

def get_orders(beerPub):
	if beerPub is None:
		return []
	return Order.query.filter_by(beerPubId=beerPub.id)

def create_order(beerPub, waiter, products, amounts, table, paidAtOrder):
	order = Order(beerPubId=beerPub.id, waiter=waiter.username, paidAtOrder=paidAtOrder, table=table)
	db.session.add(order)
	db.session.commit()

	event = get_ordered_event()
	create_order_event(order, event)
	create_order_products(order, products, amounts)
	