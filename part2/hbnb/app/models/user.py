from app.models.entity_base_class import EntityBaseClass
from app import db
from sqlalchemy.orm import validates
import re


class User(EntityBaseClass):
    __tablename__ = 'users'
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    places = db.relationship('Place',  back_populates='owner', lazy=True)
    reviews = db.relationship('Review', back_populates='user', lazy=True)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.email: str = email
        self.password: str = self.hash_password(password)
        self.is_admin: bool = is_admin

    @validates('first_name')
    def validate_first_name(self, key, first_name):
        if not isinstance(first_name, str):
            raise ValueError("First name must be a string.")
        if not first_name or len(first_name) > 50:
            raise ValueError("First name must be between 1 and 50 characters.")
        return first_name

    @validates('last_name')
    def validate_first_name(self, key, last_name):
        if not isinstance(last_name, str):
            raise ValueError("Last name must be a string.")
        if not last_name or len(last_name) > 50:
            raise ValueError("Last name must be between 1 and 50 characters.")
        return last_name

    @validates('email')
    def validate_email(self, key, email):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, email):
            raise ValueError("Invalid email address.")
        return email

    @validates('password')
    def validate_password(self, key, password):
        if not isinstance(password, str):
            raise ValueError("Password must be a string.")
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters.")
        return password

    @validates('is_admin')
    def validate_is_admin(self, key, is_admin):
        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be a boolean.")
        return is_admin

    def hash_password(self, password):
        """hashes the password using bcrypt, before returning it"""
        from app import bcrypt
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """verifies the password using bcrypt"""
        from app import bcrypt
        return bcrypt.check_password_hash(self.password, password)
