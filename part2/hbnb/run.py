from app import create_app
from app import db

app = create_app()

# dummy entities for testing
dummies = False


def create_dummies():
    from app.services import facade
    usr = dict(
        first_name='Juan',
        last_name='Aramburo',
        email='ja@a.com',
        password='pwd',
        is_admin=True
    )
    facade.create_user(usr)
    usr = dict(
        first_name='Tornelio',
        last_name='Aramburo',
        email='ta@a.com',
        password='pwd',
        is_admin=True
    )
    facade.create_user(usr)
    usr = dict(
        first_name='Orion',
        last_name='Zapata',
        email='oz@a.com',
        password='pwd',
        is_admin=False
    )
    facade.create_user(usr)
    usr = dict(
        first_name='Felipe',
        last_name='Zapata',
        email='fz@a.com',
        password='pwd',
        is_admin=False
    )
    facade.create_user(usr)

    amn = dict(name='Wifi')
    facade.create_amenity(amn)
    amn = dict(name='Swimming Pool')
    facade.create_amenity(amn)
    amn = dict(name='Air Conditioning')
    facade.create_amenity(amn)

    plc = dict(
        title='Bizancio',
        description='A cozy home near some parks',
        price=1000,
        latitude=19,
        longitude=99,
        owner_id=facade.get_all_users()[0].id
    )
    facade.create_place(plc)

    plc = dict(
        title='Casa de la abuela',
        description='A cozy home near some parks',
        price=1000,
        latitude=19,
        longitude=99,
        owner_id=facade.get_all_users()[1].id
    )
    facade.create_place(plc)

    rvw = dict(
        text='Good place',
        rating=5,
        user_id=facade.get_all_users()[0].id,
        place_id=facade.get_all_places()[0].id
    )
    facade.create_review(rvw)

    rvw = dict(
        text='Good place',
        rating=5,
        user_id=facade.get_all_users()[1].id,
        place_id=facade.get_all_places()[0].id
    )
    facade.create_review(rvw)

    rvw = dict(
        text='Good place',
        rating=5,
        user_id=facade.get_all_users()[2].id,
        place_id=facade.get_all_places()[1].id
    )
    facade.create_review(rvw)

    rvw = dict(
        text='Good place',
        rating=5,
        user_id=facade.get_all_users()[3].id,
        place_id=facade.get_all_places()[1].id
    )
    facade.create_review(rvw)

    plc = dict(
        title='Casa de la tia',
        description='A cozy home near some parks',
        price=1000,
        latitude=19,
        longitude=99,
        owner_id=facade.get_all_users()[2].id
    )
    facade.create_place(plc)

    plc = dict(
        title='Casa de la prima',
        description='A cozy home near some parks',
        price=1000,
        latitude=19,
        longitude=99,
        owner_id=facade.get_all_users()[3].id
    )


if __name__ == '__main__':
    if dummies:
        with app.app_context():
            create_dummies()
    app.run(debug=True)
