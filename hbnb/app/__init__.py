from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns


def create_app():
    """Creates and returns and instance of the Flask application"""
    app = Flask(__name__)
    api = Api(app, version='1.0',
              title='HBnB API',
              description='HBnB Application API',
              doc='/api/v1/')

    """
    API namespaces and endpoints will go here
    Other namespaces for places, review and amenities wil go here later
    """
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    return app
