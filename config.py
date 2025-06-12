import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    JWT_SECRET = os.getenv("JWT_SECRET")
    DEV_MODE = os.getenv("DEV_MODE", "False") == "True"
    SWAGGER_UI_DOC_EXPANSION = "list"

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    MONGO_URI = os.getenv("MONGO_TEST_URI", "mongodb://localhost:27017/pet_reports_test")

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False