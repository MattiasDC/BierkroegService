from flask import render_template, Blueprint
from flask_login import login_required
import http
from app.common.loginutils import admin_required
from app.models.beer_pub import BeerPub
from ..blueprint import pubmanagement_blueprint

@pubmanagement_blueprint.route('/', methods=['GET'])
@login_required
@admin_required
def home():
    return render_template('pubmanagement.html',
                            title="BierKroeg Management",
                            columns=["Start", "Einde", "Catalogus", "Acties"],
                            beer_pubs=BeerPub.get_all())

@pubmanagement_blueprint.route('/catalogus/<id>', methods=['GET'])
@login_required
@admin_required
def catalogus(id):
    beer_pub = BeerPub.get(id)
    return render_template('catalogus.html',
        title="Catalogus",
        columns=["Product", "Prijs (€)", "Acties"],
        beer_pub=beer_pub)