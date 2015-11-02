from flask import render_template, redirect, url_for, session, flash

from .. import main
from . import get_template_data
from flask_login import login_required
from app.main.forms import ServiceForm
from app import admin_api_client
from notify_client.errors import APIError


@main.route('/create-service', methods=['GET'])
@login_required
def view_create_service():
    form = ServiceForm()
    return render_template("create_service.html", form=form, **get_template_data())


@main.route('/create-service', methods=['POST'])
@login_required
def create_service():
    form = ServiceForm()
    if form.validate_on_submit():
        try:
            admin_api_client.create_service(
                form.service_name.data,
                int(session['user_id'])
            )
        except APIError as ex:
            print(ex.message)
        flash('service_created', 'success')
        return redirect(url_for('.view_dashboard'))
    else:
        return render_template("create_service.html", form=form, **get_template_data())
