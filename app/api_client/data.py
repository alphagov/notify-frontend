from __future__ import unicode_literals
from .base import BaseAPIClient
from .errors import HTTPError


class DataAPIClient(BaseAPIClient):
    def init_app(self, app):
        self.base_url = app.config['NOTIFY_DATA_API_URL']
        self.auth_token = app.config['NOTIFY_DATA_API_AUTH_TOKEN']

    def get_user_by_email_address(self, email_address):
        try:
            return self._get("/users", params={"email_address": email_address})
        except HTTPError as e:
            if e.status_code != 404:
                raise
        return None

    def get_user_by_id(self, user_id):
        try:
            return self._get("/users/{}".format(user_id))
        except HTTPError as e:
            if e.status_code != 404:
                raise
        return None

    def authenticate_user(self, email_address, password):
        try:
            return self._post(
                '/users/auth',
                data={
                    "authUsers": {
                        "emailAddress": email_address,
                        "password": password,
                    }
                })
        except HTTPError as e:
            if e.status_code not in [400, 403, 404]:
                raise
        return None
