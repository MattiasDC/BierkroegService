from .beer_pub import BeerPub
from app import db
from datetime import date

def get_beer_pub(id):
    return BeerPub.query.filter_by(id=id).one_or_none()

def create_beer_pub(startDate, endDate):
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
	today = date.today()
	return BeerPub.query.filter(BeerPub.startDate <= today,
								today <= BeerPub.endDate).one_or_none()