from app.models.entity_base_class import EntityBaseClass
from app import db
from sqlalchemy.orm import validates


class Review(EntityBaseClass):
    __tablename__ = 'reviews'
    text = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey(
        'users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey(
        'places.id'), nullable=False)

    def __init__(self, text, rating, user_id, place_id):
        super().__init__()
        self.text: str = text
        self.rating: int = rating
        self.place_id: str = place_id
        self.user_id: str = user_id

    @validates('text')
    def validate_text(self, key, text):
        if len(text) == 0:
            raise ValueError("Text cannot be empty.")
        return text

    @validates('rating')
    def validate_rating(self, key, rating):
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")
        return rating

    @validates('user_id')
    def validate_user_id(self, key, user_id):
        from app.services import facade
        if not facade.get_user(user_id):
            raise ValueError("User does not exist.")
        return user_id

    @validates('place_id')
    def validate_place_id(self, key, place_id):
        from app.services import facade
        if not facade.get_place(place_id):
            raise ValueError("Place does not exist.")
        return place_id
