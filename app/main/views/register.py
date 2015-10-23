from flask import render_template, redirect, url_for, session
from random import randint
from app import data_api_client
from .. import main
from . import get_template_data
from app.main.forms import RegistrationForm
from app.encryption import hashpw


@main.route('/register', methods=['GET'])
def render_registration_page():
    return render_template("register.html", form=RegistrationForm(), **get_template_data())


@main.route('/register', methods=['POST'])
def process_registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = data_api_client.register(form.email_address.data, form.password.data, form.mobile_number.data)
        code = ''.join(["%s" % randint(0, 9) for num in range(0, 5)])
        session['code'] = hashpw(code)
        session['user_id'] = user['user']['id']
        data_api_client.send_sms(form.mobile_number.data, code)
        return redirect(url_for('.view_3fa'))
    else:
        return render_template(
            'register.html',
            **get_template_data(form=form)
        ), 400
