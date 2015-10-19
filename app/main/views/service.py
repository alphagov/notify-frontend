from flask import render_template, session
from .. import main
from . import get_template_data
from app import data_api_client
from flask_login import login_required, current_user
from app.main.auth import role_required

@main.route('/service', methods=['GET'])
@login_required
def view_service():
    return render_template("service.html", **get_template_data())


@main.route('/services', methods=['GET'])
@login_required
def view_all_my_services():
    services = data_api_client.get_services_by_organisation_id(session['organisation_id'])
    return render_template("service.html", services=services['services'], **get_template_data())


@main.route('/services', methods=['GET'])
@login_required
@role_required('admin')
def view_all_services():
    services = data_api_client.get_services_by_organisation_id(session['organisation_id'])
    return render_template("service.html", services=services['services'], **get_template_data())
