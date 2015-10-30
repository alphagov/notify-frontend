from flask import render_template, session
from app import data_api_client
from .. import main
from . import get_template_data
from flask_login import login_required, current_user
from app.main.auth import role_required


@main.route('/service/<int:service_id>/api', methods=['GET'])
@login_required
def view_api(service_id):
    service = data_api_client.get_service_by_user_id_and_service_id(int(session['user_id']), service_id)
    usage = data_api_client.get_services_usage(service_id)['usage']
    return render_template("api.html", service=service['service'], usage=usage, **get_template_data())
