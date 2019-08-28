from flask import render_template, Blueprint, make_response
from app import dbModel, db

opdiener_blueprint = Blueprint('opdiener', __name__, url_prefix='/opdiener')

@opdiener_blueprint.route('/', methods=['GET'])
def index():
	Producten = dbModel.classes.Producten
	producten = db.session.query(Producten).all()
	return make_response(render_template('opdiener/index.html', producten=producten))