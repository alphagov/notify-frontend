from .. import main
from flask import current_app


def get_template_data(**kwargs):
    template_data = dict(main.config['BASE_TEMPLATE_DATA'], **kwargs)
    return template_data


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']
