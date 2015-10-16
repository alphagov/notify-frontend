from flask import render_template, redirect, url_for
from .. import main
from . import get_template_data
from flask_login import login_required, current_user
from app.main.forms import SmsForm
from app import data_api_client


@main.route('/service/<int:service_id>/send-sms', methods=['GET'])
@login_required
def send_sms(service_id):
    return render_template("send_sms.html", service_id=service_id, form=SmsForm(), **get_template_data())


@main.route('/service/<int:service_id>/send-sms', methods=['POST'])
def process_sms(service_id):
    form = SmsForm()
    if form.validate_on_submit():
        token = data_api_client.get_token_for_service(service_id)
        data_api_client.send_sms(form.mobile_number.data, form.message.data, token['token']['token'])
        return redirect(url_for('.view_all_jobs', service_id=service_id))
    else:
        return render_template(
            "send_sms.html",
            service_id=service_id,
            form=form,
            **get_template_data()), 400
