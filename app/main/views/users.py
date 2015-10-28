from flask import render_template, session, redirect, url_for, request, flash
from .. import main
from . import get_template_data
from app import data_api_client
from notify_client.errors import APIError
from flask_login import login_required, current_user
from app.main.forms import InviteUserForm


@main.route('/service/<int:service_id>/users', methods=['GET'])
@login_required
def view_service_users(service_id):
    service = data_api_client.get_service_by_user_id_and_service_id(int(session['user_id']), service_id)
    users = data_api_client.get_users_by_service_id(service_id)
    return render_template(
        "users.html",
        service=service['service'],
        users=users['users'],
        form=InviteUserForm(),
        **get_template_data())


@main.route('/service/<int:service_id>/add-user', methods=['POST'])
@login_required
def add_user_to_service(service_id):
    service = data_api_client.get_service_by_user_id_and_service_id(int(session['user_id']), service_id)
    users = data_api_client.get_users_by_service_id(service_id)
    form = InviteUserForm()
    if form.validate_on_submit():
        try:
            data_api_client.add_user_to_service(form.email_address.data, service_id)
            return redirect(url_for('.view_service_users', form=InviteUserForm(), service_id=service_id))
        except APIError as ex:
            flash(ex.message, "error")
            return render_template(
                'users.html',
                service=service['service'],
                users=users['users'],
                **get_template_data(form=form)
            ), 400
    else:
        return render_template(
            'users.html',
            service=service['service'],
            users=users['users'],
            **get_template_data(form=form)
        ), 400


@main.route('/service/<int:service_id>/remove-user', methods=['POST'])
@login_required
def remove_user_from_service(service_id):
    form = InviteUserForm()
    service = data_api_client.get_service_by_user_id_and_service_id(int(session['user_id']), service_id)
    users = data_api_client.get_users_by_service_id(service_id)
    try:
        data_api_client.remove_user_from_service(request.form['email_address'], service_id)
        return redirect(url_for('.view_service_users', form=InviteUserForm(), service_id=service_id))
    except APIError as ex:
        flash(ex.message, "error")
        return render_template(
            'users.html',
            service=service['service'],
            users=users['users'],
            **get_template_data(form=form)
        ), 400
