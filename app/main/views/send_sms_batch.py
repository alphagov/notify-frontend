from flask import render_template, redirect
from .. import main
from . import get_template_data
from flask_login import login_required, current_user


@main.route('/service/<int:service_id>/send-sms-batch', methods=['GET'])
@login_required
def render_send_sms_batch(service_id):
    return render_template("send_sms_batch.html", **get_template_data())


@main.route('/send-sms-batch', methods=['POST'])
def process_sms_bulk():
    return render_template("send_sms_batch.html", **get_template_data())
