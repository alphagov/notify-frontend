from flask import render_template, session
from .. import main
from . import get_template_data
from app import data_api_client
from flask_login import login_required, current_user
from app.main.auth import role_required


@main.route('/service/<int:service_id>', methods=['GET'])
@login_required
def view_service(service_id):
    service = data_api_client.get_service_by_user_id_and_service_id(int(session['user_id']), service_id)
    print(service['service'])
    return render_template("service.html", service=service['service'], **get_template_data())


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
