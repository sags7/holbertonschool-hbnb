from entity_base_class import EntityBaseClass
import re


class User(EntityBaseClass):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        first_name = first_name.strip()
        last_name = last_name.strip()
        email = email.strip()

        if len(first_name) == 0:
            raise ValueError("First name cannot be empty.")
        if len(first_name) > 50:
            raise ValueError("First name must be 50 characters or less.")
        self.first_name = first_name

        if len(last_name) == 0:
            raise ValueError("Last name cannot be empty.")
        if len(last_name) > 50:
            raise ValueError("Last name must be 50 characters or less.")
        self.last_name = last_name

        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, email):
            raise ValueError("Invalid email address.")
        self.email = email

        self.is_admin = is_admin

    def create(self):
        pass

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
