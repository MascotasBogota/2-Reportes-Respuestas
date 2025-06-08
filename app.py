from flask import Flask
from config import DevelopmentConfig
from src.extensions import api, init_db
from src.routes.report_routes import ns as reports_ns
#from src.routes.response_routes import ns as responses_ns

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    init_db(app)
    api.init_app(app)
    api.add_namespace(reports_ns, path="/reports")
    #api.add_namespace(responses_ns, path="/reports")
    return app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000)

