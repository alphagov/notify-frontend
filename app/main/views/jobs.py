from flask import render_template, session
from .. import main
from . import get_template_data
from app import admin_api_client
from flask_login import login_required, current_user


@main.route('/service/<int:service_id>/jobs', methods=['GET'])
@login_required
def view_all_jobs(service_id):
    service = admin_api_client.get_service_by_user_id_and_service_id(int(session['user_id']), service_id)
    jobs = admin_api_client.get_jobs_by_service_id(service_id)
    return render_template("jobs.html", service=service['service'], jobs=jobs['jobs'], **get_template_data())
