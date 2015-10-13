from flask import render_template, redirect
from .. import main
from . import get_template_data


@main.route('/dashboard', methods=['GET'])
def view_dashboard():
    return render_template("dashboard.html", **get_template_data())
