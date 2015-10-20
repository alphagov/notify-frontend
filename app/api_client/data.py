from __future__ import unicode_literals
from .base import BaseAPIClient
from .errors import HTTPError


class DataAPIClient(BaseAPIClient):
    def init_app(self, app):
        self.base_url = app.config['NOTIFY_DATA_API_URL']
        self.auth_token = app.config['NOTIFY_DATA_API_AUTH_TOKEN']

    def get_organisation(self, organisation_id):
        try:
            return self._get("/organisation/{}".format(organisation_id))
        except HTTPError as e:
            if e.status_code != 404:
                raise
        return None

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
                    "userAuthentication": {
                        "emailAddress": email_address,
                        "password": password,
                    }
                })
        except HTTPError as e:
            if e.status_code not in [400, 403, 404]:
                raise
        return None

    def get_service_by_user_id_and_service_id(self, user_id, service_id):
        return self._get("/user/{}/service/{}".format(user_id, service_id))

    def get_services_by_user_id(self, user_id):
        return self._get("/user/{}/services".format(user_id))

    def create_service(self, service_name, organisation_id, user_id):
        return self._post(
            '/service',
            data={
                "service": {
                    "name": service_name,
                    "organisationId": organisation_id,
                    "userId": user_id
                }
            })

    def get_jobs_by_service_id(self, service_id):
        return self._get("/service/{}/jobs".format(service_id))

    def get_notifications_by_job_id(self, job_id):
        return self._get("/job/{}/notifications".format(job_id))

    def get_notification_by_id(self, notification_id):
        return self._get("/notification/{}".format(notification_id))

    def send_sms(self, mobile_number, message, token):
        return self._post(
            '/sms/notification',
            data={
                "notification": {
                    "to": mobile_number,
                    "message": message,
                }
            }, token=token)
