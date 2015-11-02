from io import StringIO

from flask import render_template, redirect, request, url_for, session, flash
from werkzeug import secure_filename

from .. import main
from . import get_template_data
from app import admin_api_client
from app import notify_api_client
from app.csv_parser import transform
from notify_client.errors import APIError
from flask_login import login_required
from app.main.forms import CreateSMSBatchForm
from app.main.views import allowed_file


@main.route('/service/<int:service_id>/send-sms-batch', methods=['GET'])
@login_required
def render_send_sms_batch(service_id):
    service = admin_api_client.get_service_by_user_id_and_service_id(int(session['user_id']), service_id)
    return render_template(
        "send_sms_batch.html",
        form=CreateSMSBatchForm(),
        service=service['service'],
        **get_template_data()
    )


@main.route('/service/<int:service_id>/send-sms-batch', methods=['POST'])
@login_required
def process_sms_bulk(service_id):
    form = CreateSMSBatchForm()

    service = admin_api_client.get_service_by_user_id_and_service_id(int(session['user_id']), service_id)
    if form.validate_on_submit():
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
            job = admin_api_client.create_job(form.description.data, filename, service_id)
            for notification in data['notifications']:
                try:
                    notify_api_client.send_sms(
                        notification['to'],
                        notification['message'],
                        job_id=job["job"]["id"],
                        token=service['service']['token']['token']
                    )
                except APIError as ex:
                    message = "Uploaded with errors"
                    print(ex.response.json())
                    flash(message, 'error')
                    return redirect(url_for('.view_all_jobs', service_id=service_id))

            message = "Uploaded batch of {} notifications".format(len(data['notifications']))
            flash(message, 'success')
            return redirect(url_for('.view_all_jobs', service_id=service_id))
        else:
            return render_template("send_sms_batch.html", form=form, service=service['service'], **get_template_data())
    else:
        return render_template(
            "send_sms_batch.html",
            form=form,
            service=service['service'],
            **get_template_data()), 400
