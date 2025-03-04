from app.models.entity_base_class import EntityBaseClass


class Place(EntityBaseClass):
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = title.strip()
        self.description = description.strip()
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner_id
        self.create(self.title, self.description, self.price,
                    self.latitude, self.longitude, self.owner)

    def create(self, title, description, price, latitude, longitude, owner_id):
        from app.services import facade
        if not facade.get_user(owner_id):
            raise ValueError("Owner does not exist.")
        if len(title) == 0:
            raise ValueError("Title cannot be empty.")
        if len(title) > 100:
            raise ValueError("Title must be 100 characters or less.")
        if int(price) < 0:
            raise ValueError("Price cannot be lower than 0.")
        if int(latitude) < -90 or int(latitude) > 90:
            raise ValueError("Latitude must be between -90 and 90.")
        if int(longitude) < -180 or int(longitude) > 180:
            raise ValueError("Longitude must be between -180 and 180.")

        self.owner = owner_id
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.reviews = []
        self.amenities = []

        self.save()

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)

    def list_amenities(self):
        return self.amenities

    def list_reviews(self):
        return self.reviews

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
