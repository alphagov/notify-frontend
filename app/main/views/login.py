from flask import render_template, redirect, url_for, request, flash
from .. import main
from . import get_template_data
from app.main.user import User
from app.main.forms import LoginForm
from flask_login import login_user, logout_user, login_required


@main.route('/login', methods=['GET'])
def render_login():
    return render_template("login.html", form=LoginForm(), **get_template_data())


@main.route('/login', methods=['POST'])
def process_login():
    next_url = request.args.get('next')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.load_user()
        login_user(user)
        if next_url and next_url.startswith('/admin'):
            return redirect(next_url)

        return redirect(url_for('.view_service'))
    else:
        return render_template(
            'login.html',
            **get_template_data(form=form)
        ), 400


@main.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('logged_out', 'success')
    return redirect(url_for('.render_login'))
