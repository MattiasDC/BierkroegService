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