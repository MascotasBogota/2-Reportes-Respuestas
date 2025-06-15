# src/routes/images_routes.py

from flask_restx import Namespace, Resource
from flask import request, send_from_directory
from flask_jwt_extended import get_jwt_identity
from src.utils.auth import jwt_required, get_current_user_id
from src.services.image_service import handle_image_upload
import os

UPLOAD_FOLDER = 'uploads/report_images'

ns = Namespace('images', description='Subida y visualización de imágenes')

@ns.route('/upload')
class ImageUpload(Resource):
    @jwt_required
    @ns.doc(security='Bearer Auth')
    def post(self):
        file = request.files.get('image')
        if not file:
            return {"success": False, "error": "No se envió ningún archivo"}, 400

        user_id = get_current_user_id()

        success, result = handle_image_upload(file, user_id)
        if success:
            return {"success": True, "image": result}, 200
        else:
            return {"success": False, "error": result}, 400

@ns.route('/view/<string:filename>')
class ImageView(Resource):
    def get(self, filename):
        try:
            return send_from_directory(UPLOAD_FOLDER, filename)
        except FileNotFoundError:
            return {"success": False, "error": "Imagen no encontrada"}, 404
