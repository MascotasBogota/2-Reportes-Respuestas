# src/routes/images_routes.py

from flask_restx import Namespace, Resource, fields, reqparse
from werkzeug.datastructures import FileStorage
from flask import request
from flask_jwt_extended import get_jwt_identity
from src.utils.auth import jwt_required, get_current_user_id
from src.services.image_service import handle_image_upload

ns = Namespace('images', description='Subida de imágenes a Supabase Storage')

# Configurar el modelo de respuesta para Swagger
upload_response = ns.model('UploadResponse', {
    'success': fields.Boolean(description='Estado de la operación'),
    'imageUrl': fields.String(description='URL pública de la imagen subida a Supabase')
})

# Configurar el parser para subir archivos en Swagger
upload_parser = reqparse.RequestParser()
upload_parser.add_argument('image', location='files', type=FileStorage, required=True, 
                          help='Seleccione una imagen para subir (JPG, PNG, GIF)')

@ns.route('/upload')
class ImageUpload(Resource):
    @jwt_required
    @ns.doc(security='Bearer Auth')
    @ns.expect(upload_parser)
    @ns.response(200, 'Éxito', upload_response)
    @ns.response(400, 'Error en la solicitud')
    def post(self):
        args = upload_parser.parse_args()
        file = args['image']
        if not file:
            return {"success": False, "error": "No se envió ningún archivo"}, 400

        user_id = get_current_user_id()

        success, result = handle_image_upload(file, user_id)
        if success:
            return {"success": True, "imageUrl": result}, 200
        else:
            return {"success": False, "error": result}, 400
