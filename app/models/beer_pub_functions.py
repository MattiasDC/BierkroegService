from .beer_pub import BeerPub
from app import db
from datetime import date
from utils.date_utils import overlaps

def get_beer_pub(id):
    return BeerPub.query.filter_by(id=id).one_or_none()

def get_beer_pub_from_date(date):
    return BeerPub.query.filter(BeerPub.startDate <= date,
                                date <= BeerPub.endDate).one_or_none()

def overlaps_with_any(startDate, endDate, beerPub):
    return any(map(lambda bp: overlaps(startDate, endDate, bp.startDate, bp.endDate) and bp != beerPub, BeerPub.query.all()))

def create_beer_pub(startDate, endDate):
    assert(not overlaps_with_any(startDate, endDate))
    beerPub = BeerPub(startDate=startDate, endDate=endDate)
    db.session.add(beerPub)
    db.session.commit()
    return beerPub

def delete_beer_pub(beerPub):
    if beerPub is None:
        return
    db.session.delete(beerPub)
    db.session.commit()

def get_active_beer_pub():
    return get_beer_pub_from_date(date.today())
