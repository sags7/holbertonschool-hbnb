from flask_restx import Namespace, Resource, fields
from app.services import facade

from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('Users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='The user\'s first name'),
    'last_name': fields.String(required=True, description='The user\'s last name'),
    'email': fields.String(required=True, description='The user\'s email address'),
    'password': fields.String(required=True, description='The user\'s password')
})


@api.route('/')
@api.route('', strict_slashes=False)
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    # @jwt_required()
    def post(self):
        """Register a new user"""
        # current_user = get_jwt_identity()
        user_data = api.payload
        email = user_data.get('email')

        # if current_user['is_admin'] is False:
        #   return {'error': 'Admin privileges required'}, 403

        if not user_data.get('first_name') or not user_data.get('last_name') or not email:
            return {'error': 'Invalid input data'}, 400

        if not email:
            return {'message': 'Email is required'}, 400

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'message': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {'id': new_user.id,
                'first_name': new_user.first_name,
                'Last_name': new_user.last_name,
                'email': new_user.email}, 201

    def get(self):
        """Get all users"""
        users = facade.get_all_users()
        return [{'id': user.id,
                 'first_name': user.first_name,
                 'last_name': user.last_name,
                 'email': user.email,
                 # 'pass': user.password
                 }
                for user in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    # @jwt_required()
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'is_admin': user.is_admin,
                # 'password': user.password
                }, 200

    @jwt_required()
    def put(self, user_id):
        """Updates user details"""
        current_user = get_jwt_identity()
        user = facade.get_user(user_id)
        updated_data: dict = api.payload

        if current_user['is_admin'] is False:
            return {'error': 'Admin privileges required'}, 403

        if 'password' in updated_data or 'email' in updated_data and current_user['is_admin'] is False:
            return {'error': 'You cannot modify email or password'}, 400

        if not user:
            return {'error': 'User does not exist'}, 404

        if user_id != current_user['id'] and current_user['is_admin'] is False:
            return {'error': 'Unauthorized action'}, 403

        if not updated_data.get('email'):
            updated_data['email'] = user.email
        if not updated_data.get('password'):
            updated_data['password'] = user.password
        if not updated_data.get('first_name'):
            updated_data['first_name'] = user.first_name
        if not updated_data.get('last_name'):
            updated_data['last_name'] = user.last_name

        facade.update_user(user_id, updated_data)
        return {'message': 'User is successfully updated'}, 200

    @api.response(200, 'User successfully deleted')
    @api.response(404, 'User not found')
    @jwt_required()
    def delete(self, user_id):
        """Delete a user"""
        authenticatedUser = get_jwt_identity()
        userIdToDelete = user_id
        print('---------------------------------------')
        print(userIdToDelete)
        if authenticatedUser['is_admin'] is False:
            return {'error': 'Admin privileges required'}, 403

        if not facade.get_user(userIdToDelete):
            return {'error': 'User not found'}, 404

        if user_id != authenticatedUser['id'] and authenticatedUser['is_admin'] is False:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_user(userIdToDelete)
        return {'message': 'User successfully deleted'}, 200


@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user = get_jwt_identity()  # Retrieve the user's identity from the token
        return {'message': f'Hello, user {current_user["id"]}'}, 200
