from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('Users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='The user\'s first name'),
    'last_name': fields.String(required=True, description='The user\'s last name'),
    'email': fields.String(required=True, description='The user\'s email address'),
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        email = user_data.get('email')
        if not email:
            return {'message': 'Email is required'}, 400

        """Simulate email uniqueness validation"""
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'message': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {'id': new_user.id, 'first_name': new_user.first_name, 'Last_name': new_user.last_name, 'email': new_user.email}, 201

    def get(self):
        """Get all users"""
        users = facade.get_all_users()
        return [{'id': user.id,
                 'first_name': user.first_name,
                 'last_name': user.last_name,
                 'email': user.email} for user in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    def put(self, user_id):
        """Updates user details"""
        user = facade.get_user(user_id)
        updated_data = api.payload
        if not user:
            return {'error': 'User does not exist'}, 404
        facade.update_user(user_id, updated_data)
        return {'message': 'User is successfully updated'}, 200
