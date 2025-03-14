from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade


api = Namespace('Reviews', description='Review operations')


# Define the review model for input validation and documentation purposes

review_model = api.model('Review', {
    'text': fields.String(description='Description of the review'),
    'rating': fields.Integer(required=True, description='Rating of the review (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user submitting the review'),
    'place_id': fields.String(required=True, description='ID of the place being reviewed')
})


@api.route('/')
@api.route('', strict_slashes=False)
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        new_review = api.payload
        new_review['user_id'] = current_user['id']

        if not facade.get_place(new_review.get('place_id')):
            return {'message': 'Place does not exist'}, 400

        place = facade.get_place(new_review.get('place_id'))
        for review in place.reviews:
            if review.user == current_user['id']:
                return {'message': 'You have already reviewed this place'}, 400

        if place.owner == new_review.get('user_id'):
            return {'message': 'User cannot review their own place'}, 400

        if not new_review.get('text'):
            return {'message': 'Text is required'}, 400

        if int(new_review.get('rating')) < 1 or int(new_review.get('rating')) > 5:
            return {'message': 'Rating must be between 1 and 5'}, 400

        if not new_review.get('user_id'):
            return {'message': 'User ID is required'}, 400

        if not facade.get_user(new_review.get('user_id')):
            return {'message': 'User does not exist'}, 400

        if not new_review.get('place_id'):
            return {'message': 'Place ID is required'}, 400

        created_review = facade.create_review(new_review)
        return {
            "id": created_review.id,
            "text": created_review.text,
            "rating": created_review.rating,
            "user_id": created_review.user,
            "place_id": created_review.place
        }, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating
        } for review in facade.get_all_reviews()], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        current_user = get_jwt_identity()
        updated_data = api.payload

        review = facade.get_review(review_id)
        if review.user != current_user['id']:
            return {"error": 'Unauthorized action'}, 403

        if not updated_data.get('text'):
            return {'message': 'Text is required'}, 400
        if int(updated_data.get('rating')) < 1 or int(updated_data.get('rating')) > 5:
            return {'message': 'Rating must be between 1 and 5'}, 400

        facade.update_review(review_id, updated_data)
        return {"message": "Review updated successfully"}, 200

    @api.response(200, 'Review retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get all reviews for a specific place"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user,
            "place_id": review.place
        }, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        review = facade.get_review(review_id)
        current_user = get_jwt_identity()

        if not review:
            return {'error': 'Review not found'}, 404

        if current_user['is_admin'] is True or review.user == current_user['id']:
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        else:
            return {"error": 'Unauthorized action'}, 403
