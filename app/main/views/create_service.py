from flask import render_template, redirect
from .. import main
from . import get_template_data
from flask_login import login_required, current_user


@main.route('/create-service', methods=['GET'])
@login_required
def view_create_service():
    return render_template("create_service.html", **get_template_data())
