from flask import render_template, redirect, session, url_for
from .. import main
from . import get_template_data
from app.main.forms import ThreeFAForm
from app import data_api_client
from app.encryption import checkpw
from app.user import User
from flask_login import login_user


@main.route('/3fa', methods=['GET'])
def view_3fa():
    return render_template("3fa.html", form=ThreeFAForm(), **get_template_data())


@main.route('/3fa', methods=['POST'])
def submit_3fa():
    form = ThreeFAForm()
    if form.validate_on_submit():
        original_code = session['code']
        if checkpw(form.sms_code.data, original_code):
            return redirect(url_for('.view_dashboard'))
        else:
            return render_template(
                'login.html',
                **get_template_data(form=form)
            ), 403
    else:
        return render_template(
            '3fa.html',
            **get_template_data(form=form)
        ), 400
