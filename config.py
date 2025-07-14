import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    JWT_SECRET = os.getenv("JWT_SECRET")
    DEV_MODE = os.getenv("DEV_MODE", "False") == "True"
    SWAGGER_UI_DOC_EXPANSION = "list"
    SUPABASE_URL = os.getenv("SUPABASE_URL", "https://wyuefggkaclfafqumzyc.supabase.co")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sb_secret_3oZTk9WHnOfsWoTklU6sbw_NDxO7SsX")
    SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "petimages")

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    MONGO_URI = os.getenv("MONGO_TEST_URI", "mongodb://localhost:27017/pet_reports_test")

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False