from app import db
from datetime import date
from flask import current_app

class BeerPub(db.Model):
    __table_args__ = {"schema": current_app.config['DB_SCHEMA']}

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    startDate = db.Column(db.Date, nullable=False)
    endDate = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Beer Pub start<{self.startDate}> end<{self.endDate}>>'

    def is_active(self):
    	today = date.today()
    	return startDate < today and today < endDate

def get_beer_pub(id):
    return BeerPub.query.filter_by(id=id).one_or_none()

def get_active_beer_pub():
	return BeerPub.query.filter_by(active=True).one_or_none()

def create_beer_pub(startDate, endDate):
    beerPub = BeerPub(startDate=startDate, endDate=endDate)
    db.session.add(beerPub)
    db.session.commit()
    return beerPub

def delete_beer_pub(id):
    beerPub = get_beer_pub(id)
    db.session.delete(beerPub)
    db.session.commit()