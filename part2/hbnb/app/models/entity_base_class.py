import uuid
from datetime import datetime
from app import db


class EntityBaseClass(db.Model):
    __abstract__ = True  # Ensures SQLAlchemy doesn't create a table for this class
    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(),
                           onupdate=datetime.now())
