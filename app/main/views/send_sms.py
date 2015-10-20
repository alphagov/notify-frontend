from flask import render_template, redirect, url_for, session
from .. import main
from . import get_template_data
from flask_login import login_required, current_user
from app.main.forms import SmsForm
from app import data_api_client


@main.route('/service/<int:service_id>/send-sms', methods=['GET'])
@login_required
def send_sms(service_id):
    service = data_api_client.get_service_by_user_id_and_service_id(int(session['user_id']), service_id)
    return render_template("send_sms.html", service=service['service'], form=SmsForm(), **get_template_data())


@main.route('/service/<int:service_id>/send-sms', methods=['POST'])
def process_sms(service_id):
    form = SmsForm()
    if form.validate_on_submit():
        service = data_api_client.get_service_by_user_id_and_service_id(int(session['user_id']), service_id)
        data_api_client.send_sms(form.mobile_number.data, form.message.data, service['service']['token']['token'])
        return redirect(url_for('.view_all_jobs', service_id=service_id))
    else:
        return render_template(
            "send_sms.html",
            service_id=service_id,
            form=form,
            **get_template_data()), 400
