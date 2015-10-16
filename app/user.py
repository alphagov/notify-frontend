class User():
    def __init__(self, user_id, email_address, role, locked, organisation_id):
        self.id = user_id
        self.email_address = email_address
        self.role = role
        self.locked = locked
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

    @staticmethod
    def from_json(user_json):
        user = user_json["users"]
        return User(
            user_id=user["id"],
            email_address=user['emailAddress'],
            organisation_id=user['organisationId'],
            locked=user['locked'],
            role=user['role']
        )

    @staticmethod
    def load_user(data_api_client, user_id):
        """Load a user from the API and hydrate the User model"""
        user_json = data_api_client.get_user_by_id(int(user_id))

        if user_json:
            user = User.from_json(user_json)
            if user.is_active():
                return user


def user_has_role(user, role):
    try:
        return user['users']['role'] == role
    except (KeyError, TypeError):
        return False
