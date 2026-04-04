import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG = False
    TESTING = False
    SHOW_DATA_PAGE = False

class DevelopmentConfig(Config):
    DEBUG = True
    SHOW_DATA_PAGE = True

class ProductionConfig(Config):
    DEBUG = False
    SHOW_DATA_PAGE = False
