from flask import render_template, redirect
from .. import main
from . import get_template_data
from flask_login import login_required, current_user


@main.route('/view-notification-batch', methods=['GET'])
@login_required
def view_notification_batch():
    return render_template("view-notification-batch.html", **get_template_data())


@main.route('/view-notification', methods=['GET'])
@login_required
def view_notification():
    return render_template("view-notification.html", **get_template_data())
