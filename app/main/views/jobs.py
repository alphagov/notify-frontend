from flask import render_template, session
from .. import main
from . import get_template_data
from app import data_api_client
from flask_login import login_required, current_user


@main.route('/services/<int:service_id>/jobs', methods=['GET'])
@login_required
def view_all_jobs(service_id):
    jobs = data_api_client.get_jobs_by_service_id(service_id)
    return render_template("jobs.html", service_id=service_id, jobs=jobs['jobs'], **get_template_data())
