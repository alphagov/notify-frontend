from flask import render_template, redirect
from .. import main
from . import get_template_data
from flask_login import login_required, current_user
from app.main.auth import role_required


@main.route('/dashboard', methods=['GET'])
@login_required
def view_dashboard():
    return render_template("dashboard.html", **get_template_data())
