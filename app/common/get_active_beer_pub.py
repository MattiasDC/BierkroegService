from flask import abort
from app.models.beer_pub import BeerPub

def get_active_beer_pub():
	beer_pub = BeerPub.get_active()
	if beer_pub is None:
		abort(404)
	return beer_pub