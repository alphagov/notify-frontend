from flask import render_template, redirect
from .. import main
from . import get_template_data
from flask_login import login_required, current_user


@main.route('/send-sms-batch', methods=['GET'])
@login_required
def send_sms_batch():
    return render_template("send_sms_batch.html", **get_template_data())
