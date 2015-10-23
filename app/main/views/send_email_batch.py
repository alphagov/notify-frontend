from flask import render_template, redirect, request
from .. import main
from . import get_template_data
from flask_login import login_required, current_user, session, url_for
from app import data_api_client
from app.main.forms import BaseForm
from werkzeug import secure_filename
from app.main.views import allowed_file


@main.route('/service/<int:service_id>/send-email-batch', methods=['GET'])
@login_required
def render_send_email_batch(service_id):
    service = data_api_client.get_service_by_user_id_and_service_id(int(session['user_id']), service_id)
    return render_template("send_email_batch.html", form=BaseForm(), service=service['service'], **get_template_data())


@main.route('/service/<int:service_id>/send-email-batch', methods=['POST'])
@login_required
def process_email_batch(service_id):
    form = BaseForm()
    service = data_api_client.get_service_by_user_id_and_service_id(int(session['user_id']), service_id)
    file = request.files['email-bulk-upload']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        return redirect(url_for('.view_all_jobs', service_id=service_id))
    else:
        return render_template("send_sms_batch.html", form=form, service=service['service'], **get_template_data())