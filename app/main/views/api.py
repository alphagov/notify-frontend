from flask import render_template, redirect
from .. import main
from . import get_template_data
from flask_login import login_required, current_user
from app.main.auth import role_required

@main.route('/api', methods=['GET'])
@login_required
@role_required('admin')
def view_api():
    return render_template("api.html", **get_template_data())
