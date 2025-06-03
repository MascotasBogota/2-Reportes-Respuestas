from flask import Flask, jsonify
from flask_restx import Api


def create_app():
    app = Flask(__name__)
    @app.route('/',methods=["GET"])
    def home():
        return jsonify({"message":"Hello to main page :)"})
    return app