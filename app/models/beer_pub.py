from app import db

class BeerPub(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    startDate = db.Column(db.Date, nullable=False)
    endDate = db.Column(db.Date, nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Beer Pub start<{self.startDate}> end<{self.stopDate}>>'

def get_beer_pub(id):
    return BeerPub.query.filter_by(id=id).one_or_none()

def get_active_beer_pub():
	return BeerPub.query.filter_by(active=True).one_or_none()