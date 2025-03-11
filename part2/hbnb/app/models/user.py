from app.models.entity_base_class import EntityBaseClass
from app import bcrypt
import re


class User(EntityBaseClass):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip()
        self.password = password
        self.create(first_name, last_name, email, password, is_admin)

    def create(self, first_name, last_name, email, password, is_admin):

        if len(first_name) == 0:
            raise ValueError("First name cannot be empty.")
        if len(first_name) > 50:
            raise ValueError("First name must be 50 characters or less.")

        if len(last_name) == 0:
            raise ValueError("Last name cannot be empty.")
        if len(last_name) > 50:
            raise ValueError("Last name must be 50 characters or less.")

        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, email):
            raise ValueError("Invalid email address.")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.hash_password(password)

        self.save()

    def hash_password(self, password):
        """hashes the password using bcrypt, before storing it"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """verifies the password using bcrypt"""
        return bcrypt.check_password_hash(self.password, password)

    def update(self, first_name, last_name, email, is_admin):

        if first_name and len(first_name) > 0 and len(first_name) <= 50:
            self.first_name = first_name
        else:
            raise ValueError("First name must be 50 characters or less.")

        if last_name and len(last_name) > 0 and len(last_name) <= 50:
            self.last_name = last_name
        else:
            raise ValueError("Last name must be 50 characters or less.")

        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if email and re.match(email_regex, email):
            self.email = email
        else:
            raise ValueError("Invalid email address.")

        if is_admin:
            self.is_admin = is_admin

        self.save()
