from flask import render_template, session
from .. import main
from . import get_template_data
from app import data_api_client
from flask_login import login_required, current_user


@main.route('/service/<int:service_id>/users', methods=['GET'])
@login_required
def view_service_users(service_id):
    service = data_api_client.get_service_by_user_id_and_service_id(int(session['user_id']), service_id)
    users = data_api_client.get_users_by_service_id(service_id)
    return render_template("users.html", service=service['service'], users=users['users'], **get_template_data())
