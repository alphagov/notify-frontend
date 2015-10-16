from flask import render_template
from .. import main
from . import get_template_data
from flask_login import login_required, current_user
from app import data_api_client


@main.route('/view-notification-batch', methods=['GET'])
@login_required
def view_notification_batch():
    return render_template("view-notification-batch.html", **get_template_data())


@main.route('/jobs/<int:job_id>/notifications', methods=['GET'])
@login_required
def view_notification(job_id):
    notifications = data_api_client.get_notifications_by_job_id(job_id)
    return render_template(
        "view-notification.html",
        job_id=job_id,
        notifications=notifications['notifications'],
        **get_template_data())
