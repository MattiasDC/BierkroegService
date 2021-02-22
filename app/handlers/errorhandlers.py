from flask import jsonify, render_template
from flask import current_app as app

@app.errorhandler(400)
def api_error(e):
    return jsonify(error=str(e)), 400

@app.errorhandler(404)
def no_active_beer_pub(e):
	return render_template('noactivebeerpub.html'), 404