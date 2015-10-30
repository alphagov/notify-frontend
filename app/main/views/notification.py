from flask import render_template
from .. import main
from . import get_template_data
from flask_login import login_required, current_user, session
from app import data_api_client


@main.route('/view-notification-batch', methods=['GET'])
@login_required
def view_notification_batch():
    return render_template("view-notification-batch.html", **get_template_data())


@main.route('/service/<int:service_id>/job/<int:job_id>/notifications', methods=['GET'])
@login_required
def view_notification(service_id, job_id):
    job = data_api_client.get_job_by_id(job_id)
    notifications = data_api_client.get_notifications_by_job_id(job_id)
    service = data_api_client.get_service_by_user_id_and_service_id(int(session['user_id']), service_id)
    return render_template(
        "view-notification.html",
        job=job["job"],
        service=service['service'],
        notifications=notifications['notifications'],
        **get_template_data())
