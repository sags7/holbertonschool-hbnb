from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

        # dummy entities
        dummies = True

        def create_dummies(self):
            user = User(
                'Dummy Name',
                'DummyFamily',
                'dummy@dummy.com')
            user.id = 'a'
            self.user_repo.add(user)

            amenityA = Amenity('Dummy Amenity')
            amenityA.id = 'a'
            self.amenity_repo.add(amenityA)

            amenityB = Amenity('Another dummy Amenity')
            amenityB.id = 'b'
            self.amenity_repo.add(amenityB)

            place = Place(
                "DummyHome",
                "this is dummy",
                "1",
                "1",
                "1",
                self.user_repo.get_all()[0].id
            )
            place.id = 'a'
            place.amenities.append(self.amenity_repo.get_all()[0])
            place.amenities.append(self.amenity_repo.get_all()[1])
            self.place_repo.add(place)

            reviewA = Review(
                "this is a dummy review text",
                3,
                self.place_repo.get_all()[0],
                self.user_repo.get_all()[0]
            )
            reviewA.id = 'a'
            self.review_repo.add(reviewA)

            reviewB = Review(
                "Another dummy review text",
                5,
                self.place_repo.get_all()[0],
                self.user_repo.get_all()[0]
            )
            reviewB.id = 'b'
            self.review_repo.add(reviewB)

        if dummies:
            create_dummies(self)

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

    """Review CRUD operations"""

    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.add(review)
        self.get_place(review_data['place_id']).add_review(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        review.update(**review_data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        self.review_repo.delete(review_id)
        if self.review_repo.get(review_id):
            raise ValueError("Review not deleted")
