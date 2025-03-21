from app import db
from app.models.entity_base_class import EntityBaseClass
from sqlalchemy.orm import validates


class Place(EntityBaseClass):
    __tablename__ = 'places'
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Integer, nullable=False)
    longitude = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    owner = db.relationship('User' , back_populates='places', lazy=True)
    reviews = db.relationship('Review', back_populates='place', lazy=True)
    amenities = db.relationship('Amenity', secondary='place_amenities', lazy=True)

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title: str = title.strip()
        self.description: str = description.strip()
        self.price: int = price
        self.latitude: int = latitude
        self.longitude: int = longitude
        self.owner_id: str = owner_id

        from app.models.review import Review
        from app.models.amenity import Amenity
        self.reviews: list[Review] = []
        self.amenities: list[Amenity] = []

    @validates('owner_id')
    def validate_owner(self, key, owner_id):
        from app.services import facade
        if not facade.get_user(owner_id):
            raise ValueError("Owner does not exist.")
        return owner_id

    @validates('title')
    def validate_title(self, key, title):
        if len(title) == 0:
            raise ValueError("Title cannot be empty.")
        if len(title) > 100:
            raise ValueError("Title must be 100 characters or less.")
        return title

    @validates('price')
    def validate_price(self, key, price):
        if int(price) < 0:
            raise ValueError("Price cannot be lower than 0.")
        return price

    @validates('latitude')
    def validate_latitude(self, key, latitude):
        if int(latitude) < -90 or int(latitude) > 90:
            raise ValueError("Latitude must be between -90 and 90.")
        return latitude

    @validates('longitude')
    def validate_longitude(self, key, longitude):
        if int(longitude) < -180 or int(longitude) > 180:
            raise ValueError("Longitude must be between -180 and 180.")
        return longitude

    def add_review(self, review): # I may need to update commit() to or save()later
        self.reviews.append(review)
        self.save()

    def add_amenity(self, amenity): # I may need to update commit() to or save()later
        self.amenities.append(amenity)

    def list_amenities(self):
        return self.amenities

    def list_reviews(self):
        return self.reviews
