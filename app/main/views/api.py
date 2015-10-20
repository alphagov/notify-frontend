from flask import render_template, redirect
from .. import main
from . import get_template_data
from flask_login import login_required, current_user
from app.main.auth import role_required


@main.route('/service/<int:service_id>/api', methods=['GET'])
@login_required
def view_api(service_id):
    return render_template("api.html", service_id=service_id, **get_template_data())
