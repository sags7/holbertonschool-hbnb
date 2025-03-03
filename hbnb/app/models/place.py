from app.models.entity_base_class import EntityBaseClass
from app.services import facade


class Place(EntityBaseClass):
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = title.strip()
        self.description = description.strip()

        """user = facade.get_user(owner_id)
        if not user:
            raise ValueError("Owner does not exist.")"""
        self.owner = owner_id

        if len(title) == 0:
            raise ValueError("Title cannot be empty.")
        if len(title) > 100:
            raise ValueError("Title must be 100 characters or less.")
        self.title = title

        self.description = description

        if int(price) < 0:
            raise ValueError("Price cannot be lower than 0.")
        self.price = price

        if int(latitude) < -90 or int(latitude) > 90:
            raise ValueError("Latitude must be between -90 and 90.")
        self.latitude = latitude

        if int(longitude) < -180 or int(longitude) > 180:
            raise ValueError("Longitude must be between -180 and 180.")
        self.longitude = longitude

        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)

    def list_amenities(self):
        return self.amenities

    def update(self, title, description, price):

        if title and len(title) > 0 and len(title) <= 100:
            self.title = title
        else:
            raise ValueError("Title must be 100 characters or less.")

        if description and len(description) > 0:
            self.description = description

        if price and int(price) > 0:
            self.price = price

        self.save()
