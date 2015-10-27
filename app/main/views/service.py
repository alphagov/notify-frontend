from flask import render_template, session, redirect, url_for, flash
from .. import main
from . import get_template_data
from app import data_api_client
from flask_login import login_required, current_user
from app.main.auth import role_required
from app.api_client.errors import APIError
from app.main.forms import BaseForm


@main.route('/service/<int:service_id>', methods=['GET'])
@login_required
def view_service(service_id):
    service = data_api_client.get_service_by_user_id_and_service_id(int(session['user_id']), service_id)
    return render_template("service.html", form=BaseForm(), service=service['service'], **get_template_data())


@main.route('/service/<int:service_id>/activate', methods=['POST'])
@login_required
def activate_service(service_id):
    try:
        data_api_client.activate_service(service_id)
        flash("Service activated", "success")
        return redirect(url_for('.view_service', form=BaseForm(), service_id=service_id))
    except APIError as ex:
        service = data_api_client.get_service_by_user_id_and_service_id(int(session['user_id']), service_id)
        flash(ex.message, "error")
        return render_template(
            'service.html',
            service=service['service'],
            form=BaseForm(),
            **get_template_data()
        ), 400


@main.route('/service/<int:service_id>/deactivate', methods=['POST'])
@login_required
def deactivate_service(service_id):
    try:
        data_api_client.deactivate_service(service_id)
        flash("Service deactivated", "success")
        return redirect(url_for('.view_service', form=BaseForm(), service_id=service_id))
    except APIError as ex:
        service = data_api_client.get_service_by_user_id_and_service_id(int(session['user_id']), service_id)
        flash(ex.message, "error")
        return render_template(
            'service.html',
            service=service['service'],
            form=BaseForm(),
            **get_template_data()
        ), 400
