from app import create_app, db
# import all models that define db.Model tables
from app.models import user, place, review, amenity

app = create_app()

with app.app_context():
    db.create_all()
    print("Tables created successfully.")
