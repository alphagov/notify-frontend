from flask import render_template, redirect
from .. import main
from . import get_template_data
from flask_login import login_required, current_user


@main.route('/api', methods=['GET'])
@login_required
def view_api():
    return render_template("api.html", **get_template_data())
