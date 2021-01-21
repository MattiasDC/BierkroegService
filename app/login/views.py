from flask import render_template, Blueprint, request, redirect, url_for, flash, session, current_app as app
from flask_login import login_required, login_user, logout_user, current_user
from urllib.parse import urlparse
from .models import FlaskUser, get_user
from .forms import LoginForm

login_blueprint = Blueprint('login',
                            __name__,
                            url_prefix='/login',
                            template_folder="templates",
                            static_folder="static")

@login_blueprint.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.username.data)
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.rememberMe.data) 
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('main.home')
            return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@login_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.login'))