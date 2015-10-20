from flask import render_template, redirect, url_for

from .. import main
from . import get_template_data
from app.main.forms import RegistrationForm


@main.route('/register', methods=['GET'])
def render_registration_page():
    return render_template("register.html", form=RegistrationForm(), **get_template_data())


@main.route('/register', methods=['POST'])
def process_registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect(url_for('.view_dashboard'))
    else:
        return render_template(
            'register.html',
            **get_template_data(form=form)
        ), 400
