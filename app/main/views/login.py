from flask import render_template, redirect, url_for, request, flash, session

from .. import main
from . import get_template_data
from app.user import User
from app.main.forms import LoginForm
from ... import data_api_client
from flask_login import login_user, logout_user


@main.route('/login', methods=['GET'])
def render_login():
    return render_template("login.html", form=LoginForm(), **get_template_data())


@main.route('/login', methods=['POST'])
def process_login():
    next_url = request.args.get('next')
    form = LoginForm()
    if form.validate_on_submit():
        user_json = data_api_client.authenticate_user(form.email_address.data, form.password.data)
        if user_json:
            user = User.from_json(user_json)
            login_user(user)
            session['organisation_name'] = "GDS Notify"
            session['organisation_id'] = user.organisation_id
            if next_url and next_url.startswith('/admin'):
                return redirect(next_url)

            return redirect(url_for('.view_dashboard'))
        else:
            flash("no_account", "error")
            return render_template(
                "login.html",
                form=form,
                **get_template_data()), 403

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
