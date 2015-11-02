from flask import render_template, redirect, session, url_for, flash
from .. import main
from . import get_template_data
from app.main.forms import ThreeFAForm
from app import admin_api_client
from app.encryption import checkpw
from flask_login import login_user
from app import User


@main.route('/3fa', methods=['GET'])
def view_3fa():
    return render_template("3fa.html", form=ThreeFAForm(), **get_template_data())


@main.route('/3fa', methods=['POST'])
def submit_3fa():
    form = ThreeFAForm()
    if form.validate_on_submit():
        original_code = session['code']
        if checkpw(form.sms_code.data, original_code):
            user_json = admin_api_client.activate_user(session['new_user_id'])
            user = User.from_json(user_json)
            login_user(user)
            return redirect(url_for('.view_dashboard'))
        else:
            flash("invalid code", "error")
            return render_template(
                '3fa.html',
                **get_template_data(form=form)
            ), 403
    else:
        return render_template(
            '3fa.html',
            **get_template_data(form=form)
        ), 400
