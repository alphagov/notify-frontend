from flask import render_template, session
from .. import main
from . import get_template_data
from app import data_api_client
from flask_login import login_required, current_user
from app.main.auth import role_required


@main.route('/service/<int:service_id>/users', methods=['GET'])
@login_required
def view_service(service_id):
    return render_template("users.html", **get_template_data())
