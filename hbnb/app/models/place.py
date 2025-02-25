import entity_base_class as EntityBaseClass


def Place(EntityBaseClass):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        title = title.strip()
        description = description.strip()
        price = price.strip()
        latitude = latitude.strip()
        longitude = longitude.strip()
        owner = owner.strip()

        if len(title) == 0:
            raise ValueError("Title cannot be empty.")
        if len(title) > 100:
            raise ValueError("Title must be 100 characters or less.")
        self.title = title

        self.description = description

        if len(price) < 0:
            raise ValueError("Price cannot be lower than 0.")
        self.price = price

        if latitude < -90 or latitude > 90:
            raise ValueError("Latitude must be between -90 and 90.")
        self.latitude = latitude

        if longitude < -180 or longitude > 180:
            raise ValueError("Longitude must be between -180 and 180.")
        self.longitude = longitude

        """!!!!!Need to validate existence of owner in DB"""
        self.owner = owner
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)

    def list_amenities(self):
        return self.amenities

    """not implemented yet"""

    def create(self):
        pass

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
