from app.persistence.repository import InMemoryRepository
from app.models.user import User


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()  # lista de objetos???
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    """Placeholder for creating a User"""
    """instantiates a User object adds it to the user repository and user_repo becomes a list of users"""

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    """returns a dictionary with all the user data"""

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        user.update(**user_data)

        return self.user_repo.get(user_id)
