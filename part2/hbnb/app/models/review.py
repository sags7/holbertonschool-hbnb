from app.models.entity_base_class import EntityBaseClass


class Review(EntityBaseClass):
    def __init__(self, text, rating, user_id, place_id):
        super().__init__()
        self.text = text.strip()
        self.create(text, rating, user_id, place_id,)

    def create(self, text, rating, user_id, place_id):

        if len(text) == 0:
            raise ValueError("Text cannot be empty.")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")
        
        import app.services.facade as facade
        
        if not facade.get_user(user_id):
            raise ValueError("User does not exist.")
        if not facade.get_place(place_id):
            raise ValueError("Place does not exist.")

        self.text = text
        self.rating = rating
        self.place = place_id
        self.user = user_id

        self.save()

    def update(self, text, rating):
        if len(text) == 0:
            raise ValueError("Text cannot be empty.")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")

        self.text = text.strip()
        self.rating = rating

        self.save()
