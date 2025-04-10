import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)         # 1 hour access token
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
