from flask_restx import Api
from mongoengine import connect
from flask import current_app

api = Api(   
   #Inicialización de la API de PatitasBog    
    title="PatitasBog - Reportes y respuestas API",
    version="1.0",
    description="Servicio de reportes y respuestas"
)

def init_db(app):
    """
    Initialize the MongoDB connection using the URI from the app's config.
    """
    connect(host=app.config["MONGO_URI"])