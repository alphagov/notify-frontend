from flask import render_template, redirect, url_for, request, flash, session

from .. import main
from . import get_template_data
from app.user import User
from app.main.forms import InviteUserForm
from ... import data_api_client
from flask_login import login_required


@main.route('/service/<int:service_id>/invite-a-user', methods=['GET'])
@login_required
def render_invite_a_user(service_id):
    service = data_api_client.get_service_by_user_id_and_service_id(int(session['user_id']), service_id)
    return render_template(
        "invite_a_user.html",
        service=service['service'],
        form=InviteUserForm(),
        **get_template_data())


@main.route('/service/<int:service_id>/invite-a-user', methods=['POST'])
@login_required
def process_invite_a_user(service_id):
    form = InviteUserForm()
    service = data_api_client.get_service_by_user_id_and_service_id(int(session['user_id']), service_id)
    if form.validate_on_submit():
        return redirect(url_for('.view_dashboard'))
    else:
        return render_template(
            'invite_a_user.html',
            service=service['service'],
            **get_template_data(form=form)
        ), 400
