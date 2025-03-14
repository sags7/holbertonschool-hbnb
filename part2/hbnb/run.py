from app.models.review import Review
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.user import User
from app import create_app

app = create_app()

# dummy entities for testing
dummies = True


def create_dummies():
    from app.services import facade
    


if dummies:
    create_dummies()
if __name__ == '__main__':
    app.run(debug=True)
