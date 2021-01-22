from flask import render_template, Blueprint, abort, request, current_app as app, jsonify
from flask_login import login_required
from app.models.beer_pub_product_functions import get_beer_pub_products
from app.models.beer_pub_functions import get_active_beer_pub
from app.models.product_functions import get_product
from app.login.utils import admin_required
from app.login.models import get_users, get_user, create_user, delete_user, has_user_with_name
import http

waiter_blueprint = Blueprint('waiter', __name__,
							 url_prefix='/waiter',
                             template_folder="templates",
                             static_folder="static")

@waiter_blueprint.errorhandler(400)
def api_error(e):
    return jsonify(error=str(e)), 400

@waiter_blueprint.route('/waiter', methods=['GET'])
@login_required
def waiter():
	return render_template('waiter.html',
		products=get_beer_pub_products(get_active_beer_pub()),
		get_product=get_product)

@waiter_blueprint.route('/management', methods=['GET'])
@login_required
@admin_required
def waiter_management():
	return render_template('waitermanagement.html',
							title="Opdiener Management",
							columns=["Naam", "Acties"],
							waiters=filter(lambda user: not user.is_admin(), get_users()))


@waiter_blueprint.route('/create', methods=['POST'])
@login_required
@admin_required
def create():
	name = request.form['name']
	if has_user_with_name(name):
		abort(400, "A waiter with the same name already exists")
	waiter = create_user(name, app.config['USER_PWD'], False)
	return jsonify(waiter.get_id())

@waiter_blueprint.route('/delete', methods=['POST'])
@login_required
@admin_required
def delete():
	waiter = get_user(request.form['name'])
	delete_user(waiter)
	return ("", http.HTTPStatus.NO_CONTENT)