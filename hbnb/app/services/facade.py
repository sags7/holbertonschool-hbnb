from app.persistance.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    """Placeholder for creating a User"""
    def create_user(self, user_data):
        #implementation pending
        pass

    def get_place(self, place_id):
        #implementation pending
        pass
    