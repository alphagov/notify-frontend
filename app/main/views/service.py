from flask import render_template, session, redirect, url_for, flash
from .. import main
from . import get_template_data
from app import data_api_client
from flask_login import login_required, current_user
from app.main.auth import role_required
from notify_client.errors import APIError
from app.main.forms import BaseForm
from datetime import datetime


@main.route('/service/<int:service_id>', methods=['GET'])
@login_required
def view_service(service_id):
    service = data_api_client.get_service_by_user_id_and_service_id(int(session['user_id']), service_id)
    usage = data_api_client.get_services_usage(service_id)['usage']
    today = datetime.utcnow().date()
    used_today = 0
    for use in usage:
        if use['day'] == str(today):
            used_today = use['count']

    return render_template(
        "service.html",
        form=BaseForm(),
        used_today=used_today,
        service=service['service'],
        **get_template_data())


@main.route('/service/<int:service_id>/activate', methods=['POST'])
@login_required
def activate_service(service_id):
    try:
        data_api_client.activate_service(service_id)
        flash("Service activated", "success")
        return redirect(url_for('.view_service', service_id=service_id))
    except APIError as ex:
        flash(ex.message, "error")
        return redirect(url_for('.view_service', service_id=service_id))


@main.route('/service/<int:service_id>/deactivate', methods=['POST'])
@login_required
def deactivate_service(service_id):
    try:
        data_api_client.deactivate_service(service_id)
        flash("Service deactivated", "success")
        return redirect(url_for('.view_service', service_id=service_id))
    except APIError as ex:
        flash(ex.message, "error")
        return redirect(url_for('.view_service', service_id=service_id))
