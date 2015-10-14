from __future__ import unicode_literals
from .base import BaseAPIClient
from .errors import HTTPError


class DataAPIClient(BaseAPIClient):
    def init_app(self, app):
        self.base_url = app.config['NOTIFY_DATA_API_URL']
        self.auth_token = app.config['NOTIFY_DATA_API_AUTH_TOKEN']

    def get_user(self, user_id=None):
        try:
            user = self._get("/users/{}".format(user_id))

            if isinstance(user['users'], list):
                user['users'] = user['users'][0]

            return user

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
