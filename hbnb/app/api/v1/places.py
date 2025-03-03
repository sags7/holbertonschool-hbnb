from flask_restx import Namespace, Resource, fields
from app.services import facade

"""This is the namespace for the Place API"""
api = Namespace('Places', description='Place operations')

"""These models are for input validation and documentation purposes"""
place_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'User': fields.String(required=True, description='The user\'s first name'),
    'last_name': fields.String(required=True, description='The user\'s last name'),
    'email': fields.String(required=True, description='The user\'s email address'),
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'Longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=False, description='List of amenity IDs')
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        place_data = api.payload
        if not place_data.get('title'):
            return {'message': 'Title is required'}, 400
        if len(place_data.get('title')) > 50:
            return {'message': 'Title must be 50 characters or less'}, 400

        if not place_data.get('price'):
            return {'message': 'Price is required'}, 400
        if (int(place_data.get('price'))) < 0:
            return {'message': 'Price cannot be lower than 0'}, 400

        if not place_data.get('latitude'):
            return {'message': 'Latitude is required'}, 400
        if int(place_data.get('latitude')) < -90 or int(place_data.get('latitude')) > 90:
            return {'message': 'Latitude must be from -90 to 90'}, 400

        if not place_data.get('longitude'):
            return {'message': 'Longitude is required'}, 400
        if int(place_data.get('longitude')) < -90 or int(place_data.get('latitude')) > 90:
            return {'message': 'Longitude must be from -90 to 90'}, 400

        if not place_data.get('owner_id'):
            return {'message': 'Owner ID is required'}, 400
        if not facade.get_user(place_data.get('owner_id')):
            return {'message': 'Owner does not exist'}, 400

        new_place = facade.create_place(place_data)
        return {
            'id': new_place.id,
            'title': new_place.title,
            'description': new_place.description,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'owner_id': new_place.owner
        }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        places_list = facade.get_all_places()
        return [{
            'id': place.id,
            'title': place.title,
            # 'description': place.description,
            # 'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            # 'owner_id': place.owner
        } for place in places_list], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        place = facade.get_place(place_id)
        user = facade.get_user(place.owner)
        if not place:
            return {'error': 'Place not found'}, 404
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            },
            'amenities': [{
                'id': amenity.id,
                'name': amenity.name
            } for amenity in place.amenities]

        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place details updated successfully')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        place = facade.get_place(place_id)
        updated_data = api.payload
        if not place:
            return {'error': 'Place not found'}, 404
        facade.update_place(place_id, updated_data)
        return {
            'message': 'Place updated successfully'}, 200


# PUT /api/v1/places/<place_id>: Update place information.
