import entity_base_class as EntityBaseClass


class Review(EntityBaseClass):
    def __init__(self, text, rating, place, user):
        super().__init__()
        text = text.strip()
        rating = rating.strip()
        place = place.strip()
        user = user.strip()

        if len(text) == 0:
            raise ValueError("Text cannot be empty.")
        self.text = text

        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")
        self.rating = rating

        """!!!Place and User havent been linked to the repository yet"""
        self.place = place
        self.user = user

    def create(self):
        pass

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
