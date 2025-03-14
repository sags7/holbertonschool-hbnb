from app.models.review import Review
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.user import User
from app import create_app

app = create_app()

# dummy entities for testing
dummies = False


def create_dummies():
    from app.services import facade

    user = User(
        'Admin',
        'One',
        'admin@one.com',
        'pwd',
        True)
    user.id = 'a'
    facade.user_repo.add(user)

    """user = User(
        'Dummy',
        'Family',
        'dummy@dummy.com',
        'pwd')
    user.id = 'b'
    facade.user_repo.add(user)

    amenityA = Amenity('Dummy Amenity')
    amenityA.id = 'a'
    facade.amenity_repo.add(amenityA)

    amenityB = Amenity('Another dummy Amenity')
    amenityB.id = 'b'
    facade.amenity_repo.add(amenityB)

    place = Place(
        "DummyHome",
        "this is dummy",
        "1",
        "1",
        "1",
        "a"
    )
    place.id = 'a'
    place.amenities.append(facade.amenity_repo.get_all()[0])
    place.amenities.append(facade.amenity_repo.get_all()[1])
    facade.place_repo.add(place)

    reviewA = Review(
        "this is a dummy review text",
        3,
        'a',
        'a'
    )
    reviewA.id = 'a'
    facade.review_repo.add(reviewA)

    reviewB = Review(
        "Another dummy review text",
        5,
        'a',
        'a'
    )
    reviewB.id = 'b'
    facade.review_repo.add(reviewB)"""


if dummies:
    create_dummies()
if __name__ == '__main__':
    app.run(debug=True)
