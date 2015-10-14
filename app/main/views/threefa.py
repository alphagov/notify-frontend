from flask import render_template, redirect
from .. import main
from . import get_template_data
from flask_login import login_required, current_user


@main.route('/3fa', methods=['GET'])
@login_required
def view_3fa():
    return render_template("3fa.html", **get_template_data())
