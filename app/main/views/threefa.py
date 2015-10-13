from flask import render_template, redirect
from .. import main
from . import get_template_data


@main.route('/3fa', methods=['GET'])
def view_3fa():
    return render_template("3fa.html", **get_template_data())
