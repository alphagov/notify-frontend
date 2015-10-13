from flask import Blueprint


main = Blueprint('main', __name__)

from .views import login, service, view, create_service, threefa, dashboard


@main.after_request
def add_cache_control(response):
    response.cache_control.no_cache = True
    return response
