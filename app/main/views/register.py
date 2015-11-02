
from flask import render_template, redirect, url_for, session, flash
from random import randint
from app import data_api_client
from .. import main
from . import get_template_data
from app.main.forms import RegistrationForm
from app.encryption import hashpw
from notify_client.errors import HTTPError, APIError


@main.route('/register', methods=['GET'])
def render_registration_page():
    return render_template("register.html", form=RegistrationForm(), **get_template_data())


@main.route('/register', methods=['POST'])
def process_registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = data_api_client.register(form.email_address.data, form.password.data, form.mobile_number.data)
            code = ''.join(["%s" % randint(0, 9) for num in range(0, 5)])
            session['code'] = hashpw(code)
            session['new_user_id'] = user['users']['id']
            data_api_client.send_sms(form.mobile_number.data, code)
            return redirect(url_for('.view_3fa'))
        except APIError as e:
            print(e.response.json())
            flash("Error creating user", "error")
            return render_template(
                'register.html',
                **get_template_data(form=form)
            ), 400

    else:
        return render_template(
            'register.html',
            **get_template_data(form=form)
        ), 400
