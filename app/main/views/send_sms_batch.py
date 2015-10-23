from flask import render_template, redirect, current_app, request, url_for, session
from .. import main
from . import get_template_data
from app import data_api_client
from app.csv_parser import transform
from flask_login import login_required, current_user
from werkzeug import secure_filename
from app.main.forms import BaseForm
from app.main.views import allowed_file
from io import StringIO


@main.route('/service/<int:service_id>/send-sms-batch', methods=['GET'])
@login_required
def render_send_sms_batch(service_id):
    service = data_api_client.get_service_by_user_id_and_service_id(int(session['user_id']), service_id)
    return render_template("send_sms_batch.html", form=BaseForm(), service=service['service'], **get_template_data())


@main.route('/service/<int:service_id>/send-sms-batch', methods=['POST'])
@login_required
def process_sms_bulk(service_id):
    form = BaseForm()
    service = data_api_client.get_service_by_user_id_and_service_id(int(session['user_id']), service_id)
    uploaded = request.files['sms-bulk-upload']
    if uploaded and allowed_file(uploaded.filename):
        filename = secure_filename(uploaded.filename)
        data = transform(StringIO(uploaded.stream.read().decode("UTF8")), 'sms')
        if 'errors' in data:
            return render_template(
                "send_sms_batch.html",
                form=form,
                errors=data['errors'],
                service=service['service'],
                **get_template_data()
            ), 400
        job = data_api_client.create_job(filename, service_id)
        for notification in data['notifications']:
            data_api_client.send_sms(
                notification['to'],
                notification['message'],
                job["job"]["id"],
                service['service']['token']['token']
            )
        return redirect(url_for('.view_all_jobs', service_id=service_id))
    else:
        return render_template("send_sms_batch.html", form=form, service=service['service'], **get_template_data())
