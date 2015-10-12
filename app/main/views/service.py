from flask import render_template, redirect
from .. import main
from . import get_template_data


@main.route('/service', methods=['GET'])
def view_service():
    return render_template("service.html", **get_template_data())




