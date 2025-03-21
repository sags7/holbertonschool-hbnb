from app.models.entity_base_class import EntityBaseClass
from app import db
from sqlalchemy.orm import validates


class Amenity(EntityBaseClass):
    __tablename__ = 'amenities'
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name: str):
        super().__init__()
        self.name: str = name

    @validates('name')
    def validate_name(self, key, name):
        if len(name) == 0:
            raise ValueError("Name cannot be empty.")
        if len(name) > 50:
            raise ValueError("Name must be 50 characters or less.")
        return name


class PlaceAmenity(db.Model):
    __tablename__ = 'place_amenities'
    place_id = db.Column(
        db.String(36),
        db.ForeignKey('places.id'),
        primary_key=True
    )
    amenity_id = db.Column(
        db.String(36),
        db.ForeignKey('amenities.id'),
        primary_key=True
    )
