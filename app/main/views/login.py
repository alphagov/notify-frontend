from flask import render_template, redirect, url_for
from .. import main
from . import get_template_data


@main.route('/login', methods=['GET'])
def render_login():
    return render_template("login.html", **get_template_data())


@main.route('/login', methods=['POST'])
def submit_login():
    return redirect(url_for('.view_service'))
