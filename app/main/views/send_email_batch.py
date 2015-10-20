from flask import render_template, redirect
from .. import main
from . import get_template_data
from flask_login import login_required, current_user


@main.route('/service/<int:service_id>/send-email-batch', methods=['GET'])
@login_required
def render_send_email_batch(service_id):
    return render_template("send_email_batch.html", **get_template_data())
