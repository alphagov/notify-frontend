from flask import json


def user_has_role(user, role):
    try:
        return user['users']['role'] == role
    except (KeyError, TypeError):
        return False


class User():
    def __init__(self, user_id, email_address, role, organisation_id):
        self.id = user_id
        self.email_address = email_address
        self.role = role
        self.organisation_id = organisation_id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_locked(self):
        return self.locked

    def is_anonymous(self):
        return False

    def has_role(self, role):
        return self.role == role

    def get_id(self):
        return str(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'emailAddress': self.email_address,
            'organisationId': self.organisation_id,
            'role': self.role
        }

    @staticmethod
    def from_json(user_json):
        user = user_json["users"]
        return User(
            user_id=user["id"],
            email_address=user['emailAddress'],
            organisation_id=user['organisationId'],
            role=user['role']
        )

    @staticmethod
    def load_user():
        """Load a user from the API and hydrate the User model"""
        # user_json = data_api_client.get_user(user_id=int(user_id))

        user_json = {'users': {
            'id': 1234,
            'emailAddress': 'test@example.com',
            'active': True,
            'locked': False,
            'role': 'admin',
            'organisationId': 1234
        }}

        if user_json:
            user = User.from_json(user_json)
            if user.is_active():
                return user
