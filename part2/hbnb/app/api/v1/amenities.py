from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('Amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
@api.route('', strict_slashes=False)
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Create a new amenity"""
        current_user = get_jwt_identity()
        amenity_data = api.payload

        if current_user['is_admin'] is False:
            return {'error': 'Admin privileges required'}, 403

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
    @jwt_required()
    def put(self, amenity_id):
        """Updates Amenity details"""
        current_user = get_jwt_identity()
        amenity = facade.get_amenity(amenity_id)
        updated_data = api.payload

        if current_user['is_admin'] is False:
            return {'error': 'Admin privileges required'}, 403

        if not amenity:
            return {'message': 'Error: Amenity not found'}, 404
        facade.update_amenity(amenity_id, updated_data)
        return {'message': 'Amenity is successfully updated'}, 200
