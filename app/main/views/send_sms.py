from flask import render_template, redirect
from .. import main
from . import get_template_data
from flask_login import login_required, current_user


@main.route('/send-sms', methods=['GET'])
@login_required
def view_service():
    return render_template("send_sms.html", **get_template_data())
