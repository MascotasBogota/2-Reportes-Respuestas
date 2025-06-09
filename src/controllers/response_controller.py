from flask import jsonify, request
from src.services.response_service import create_response_service, ServiceError
#from src.utils.auth import get_current_user_id

def add_response_controller(report_id):
    user_id = get_current_user_id()
    if not user_id:
        return {'message': 'Token inválido o no autenticado'}, 401

    data = request.get_json() or {}
    try:
        result = create_response_service(report_id, data, user_id)
        return jsonify(result), 201

    except ServiceError as se:
        # Errores controlados (404, 403, 400 según mensaje)
        msg = str(se)
        if msg == 'Reporte no encontrado':
            return {'message': msg}, 404
        if msg == 'No se pueden agregar respuestas a un reporte cerrado':
            return {'message': msg}, 403
        if msg == 'Usuario no existe':
            return {'message': msg}, 400
        # fallback
        return {'message': msg}, 400

    except Exception:
        return {'message': 'Error interno al crear respuesta'}, 500