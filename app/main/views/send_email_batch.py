from flask import render_template, redirect
from .. import main
from . import get_template_data
from flask_login import login_required, current_user


@main.route('/send-email-batch', methods=['GET'])
@login_required
def email():
    return render_template("send_email_batch.html", **get_template_data())
