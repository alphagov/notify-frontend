from flask import render_template, redirect
from .. import main
from . import get_template_data


@main.route('/create-service', methods=['GET'])
def view_create_service():
    return render_template("create-service.html", **get_template_data())




