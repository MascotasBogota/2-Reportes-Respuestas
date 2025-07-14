# src/routes/images_routes.py

from flask_restx import Namespace, Resource
from flask import request
from flask_jwt_extended import get_jwt_identity
from src.utils.auth import jwt_required, get_current_user_id
from src.services.image_service import handle_image_upload

ns = Namespace('images', description='Subida de imágenes a Supabase Storage')

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
            return {"success": True, "imageUrl": result}, 200
        else:
            return {"success": False, "error": result}, 400
