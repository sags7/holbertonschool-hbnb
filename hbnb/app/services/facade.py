from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

        # dummy entities
        self.user_repo.add(User(
            'Dummy Name',
            'DummyFamily',
            'dummy@dummy.com'))

        self.amenity_repo.add(Amenity('Dummy Amenity'))
        self.amenity_repo.add(Amenity('Another Dummy Amenity'))

        self.place_repo.add(Place(
            "DummyHome",
            "this is dummy",
            "1",
            "1",
            "1",
            self.user_repo.get_all()[0].id
        ))
        place = self.place_repo.get_all()[0]
        amenity = self.amenity_repo.get_all()[0]
        place.add_amenity(amenity)
        amenity = self.amenity_repo.get_all()[1]
        place.add_amenity(amenity)

    """User CRUD operations"""

    def create_user(self, user_data):
        """
            instantiates a User object adds it to the user repository
            Returns: User object
        """
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """returns a User object from the user repository"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        user.update(**user_data)
        return self.user_repo.get(user_id)

    """Amenity CRUD operations"""

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Returns the Amenity object in the repo by id"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        amenity.update(amenity_data['name'])
        return self.user_repo.get(amenity_id)

    """Place CRUD operations"""

    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        place.update(**place_data)
        return self.place_repo.get(place_id)
