from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('Amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        amenity_data = api.payload
        print(api.payload)
        if len(amenity_data['name']) > 50:
            return {'message': 'Name must be less than 50 characters long'}, 400

        new_amenity = facade.create_amenity(amenity_data)
        return {'id': new_amenity.id,
                'name': new_amenity.name}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        all_amenities = facade.get_all_amenities()
        return [{'id': amenity.id, 'name': amenity.name}
                for amenity in all_amenities], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'message': 'Error: Amenity not found'}, 404
        return {'id:': amenity.id, 'name': amenity.name}

    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Updates Amenity details"""
        amenity = facade.get_amenity(amenity_id)
        updated_data = api.payload
        if not amenity:
            return {'message': 'Error: Amenity not found'}, 404
        facade.update_amenity(amenity_id, updated_data)
        return {'message': 'Amenity is successfully updated'}, 200
