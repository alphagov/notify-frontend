from io import StringIO

from flask import render_template, redirect, request, flash
from .. import main
from . import get_template_data
from flask_login import login_required, current_user, session, url_for
from app import admin_api_client
from app.main.forms import CreateEmailBatchForm
from werkzeug import secure_filename
from app.main.views import allowed_file
from notify_client.errors import APIError

from app.csv_parser import transform


@main.route('/service/<int:service_id>/send-email-batch', methods=['GET'])
@login_required
def render_send_email_batch(service_id):
    service = admin_api_client.get_service_by_user_id_and_service_id(int(session['user_id']), service_id)
    return render_template("send_email_batch.html",
                           form=CreateEmailBatchForm(),
                           service=service['service'],
                           **get_template_data())


@main.route('/service/<int:service_id>/send-email-batch', methods=['POST'])
@login_required
def process_email_batch(service_id):
    print("start process_email_batch")
    form = CreateEmailBatchForm()
    service = admin_api_client.get_service_by_user_id_and_service_id(int(session['user_id']), service_id)
    file = request.files['email-bulk-upload']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        data = transform(StringIO(file.stream.read().decode("UTF8")), 'email')
        if 'errors' in data:
            return render_template("send_sms_batch.html",
                                   form=form,
                                   errors=data['errors'],
                                   service=service['service'],
                                   **get_template_data()
                                   ), 400
        job = admin_api_client.create_job(form.description.data, filename, service_id)
        print("job {}".format(job))
        print(data)
        for notification in data['notifications']:
            print("**noifitcation {}".format(notification))
            try:
                admin_api_client.send_email(
                    notification['to'],
                    notification["message"],
                    notification["from"],
                    notification["subject"],
                    job_id=job["job"]["id"],
                    token=service["service"]["token"]["token"])
            except APIError as ex:
                message = "Upload with errors"
                print(ex.response.json())
                flash(message, 'error')
                return redirect(url_for('.view_all_jobs', service_id=service_id))
        message = "Uploaded email batch of {} notifications".format(len(data["notifications"]))
        flash(message, 'success')
        return redirect(url_for('.view_all_jobs', service_id=service_id))

    else:
        return render_template(
            "send_email_batch.html",
            form=form,
            service=service['service'],
            **get_template_data()), 400
