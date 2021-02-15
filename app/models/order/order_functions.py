from app import db
from .order import Order
from .orderproduct import OrderProduct
from .event import get_ordered_event, get_ordered_event_id
from .orderevent import create_order_event, OrderEvent, delete_order_events
from app.models.beer_pub_functions import get_beer_pub
from app.models.product.beer_pub_product_functions import get_beer_pub_product
from app.models.product.product_functions import get_product

def get_orders(beerPub):
    if beerPub is None:
        return []
    return Order.query.filter_by(beerPubId=beerPub.id)

def get_order(orderId):
    return Order.query.filter_by(id=orderId).one_or_none()

def create_order(beerPub, waiter, products, amounts, table, paidAtOrder, remarks=""):
    order = Order(beerPubId=beerPub.id, waiter=waiter.username, paidAtOrder=paidAtOrder, table=table, remarks=remarks)
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

def delete_orders(beerPub):
    orders = Order.query.filter_by(beerPubId=beerPub.id)
    for order in orders:
        delete_order(order)

def create_order_products(order, products, amounts):
    assert(len(products) == len(amounts))
    orderProducts = [OrderProduct(orderId=order.id, productId=product.id, amount=amount) for product, amount in zip(products, amounts)]
    for orderProduct in orderProducts:
        db.session.add(orderProduct)
    db.session.commit()
    return orderProducts

def delete_order_products(order):
    orderProducts = OrderProduct.query.filter_by(orderId=order.id)
    for orderProduct in orderProducts:
        db.session.delete(orderProduct)
    db.session.commit()

def get_order_products(order):
    return OrderProduct.query.filter_by(orderId=order.id)

def get_order_product_price(orderProduct):
    beerPub = get_beer_pub(get_order(orderProduct.orderId).beerPubId)
    return orderProduct.amount*get_beer_pub_product(beerPub, get_product(orderProduct.productId)).price

def get_order_total_price(order):
    return sum(map(lambda op: get_order_product_price(op), get_order_products(order)))