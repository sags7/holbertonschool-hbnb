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

    def save(self):
        self.updated_at = datetime.now()
        db.session.commit()

    def update(self, data: dict):
        for key, value in data.items():
            if key == 'id' or key == 'created_at' or key == 'updated_at' or key == 'owner_id':
                continue
            if hasattr(self, key):
                if key == 'amenities' and isinstance(value, list):
                    # Convert amenity IDs to Amenity instances
                    from app.models.amenity import Amenity
                    amenity_instances = []
                    for amenity_id in value:
                        amenity = db.session.get(Amenity, amenity_id)
                        if amenity:
                            amenity_instances.append(amenity)
                    setattr(self, key, amenity_instances)
                else:
                    setattr(self, key, value)
        self.save()
