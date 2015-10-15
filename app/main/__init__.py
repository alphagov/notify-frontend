from flask import Blueprint

main = Blueprint('main', __name__)


@main.after_request
def add_cache_control(response):
    response.cache_control.no_cache = True
    return response

from app.main.views import login, service, view, create_service, threefa, dashboard, send_sms,
    send_sms_batch, send_email_batch
