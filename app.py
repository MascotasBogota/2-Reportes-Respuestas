from flask import Flask
from config import DevelopmentConfig
from src.extensions import api, init_db
from src.routes.report_routes import ns as reports_ns
from src.routes.response_routes import ns as responses_ns  
from src.routes.images_routes import ns as images_ns  

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa base de datos y API Swagger
    init_db(app)
    api.init_app(app)

    # Registra los endpoints de /reports
    api.add_namespace(reports_ns, path="/reports")
    api.add_namespace(responses_ns, path="/responses")
    api.add_namespace(images_ns, path="/images")
    return app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000)