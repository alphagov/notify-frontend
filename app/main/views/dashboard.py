from flask import render_template, session
from .. import main
from . import get_template_data
from flask_login import login_required, current_user
from app import admin_api_client


@main.route('/dashboard', methods=['GET'])
@login_required
def view_dashboard():
    services = admin_api_client.get_services_by_user_id(session['user_id'])
    return render_template("dashboard.html", services=services["services"], **get_template_data())
