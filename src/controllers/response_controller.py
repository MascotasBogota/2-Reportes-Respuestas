from flask import jsonify, request
from src.services.response_service import create_response_service,get_response_service,get_all_responses_service, ServiceError, update_response_service, delete_response_service
from src.utils.auth import get_current_user_id
from src.utils.serialization import serialize_response
from flask_restx import abort



def add_response_controller(report_id):
    user_id = get_current_user_id()
    if not user_id:
        return {'message': 'Token inválido o no autenticado'}, 401

    data = request.get_json() or {}
    try:
        result = create_response_service(report_id, data, user_id)
        print(f"Response created: {result}")
        return serialize_response(result), 201

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

    except Exception as e:
        return {'message': str(e)}, 500
    
def get_response_controller(report_id, response_id):
    try:
        result = get_response_service(report_id, response_id)
        return serialize_response(result), 200

    except ServiceError as se:
        # Errores controlados (404, 403, 400 según mensaje)
        msg = str(se)
        if msg == 'Reporte no encontrado' or msg == 'Respuesta no encontrada':
            return {'message': msg}, 404
        # fallback
        return {'message': msg}, 400

    except Exception as e:
        return {'message': str(e)}, 500

def get_all_responses_controller(report_id):
    try:
        result = get_all_responses_service(report_id)
        result = [serialize_response(res) for res in result]
        return result
    except ServiceError as se:
        # Errores controlados (404, 403, 400 según mensaje)
        msg = str(se)
        if msg == 'Reporte no encontrado' or msg == 'No hay ninguna respuesta para este reporte':
            return {'message': msg}, 404
        # fallback
        return {'message': msg}, 400

    except Exception as e:
        return {'message': str(e)}, 500

def update_response_controller(report_id, response_id):
    try:
        user_id = get_current_user_id()
        print(f"user is {user_id}")
        data = request.json
        updated_response = update_response_service(report_id,response_id,data,user_id)
        return serialize_response(updated_response)
    except ServiceError as se:
        msg = str(se)
        if msg == 'Reporte no encontrado' or msg == 'Respuesta no encontrada':
            return {'message': msg}, 404
        if msg == 'No se pueden cambiar respuestas de un reporte cerrado' or msg == 'Usuarios solo pueden modificar sus propias respuestas':
            return {'message': msg}, 403
        if msg == 'Usuario no existe':
            return {'message': msg}, 400
        # fallback
        return {'message': msg}, 400

    except Exception as e:
        return {'message': str(e)}, 500

def delete_response_controller(report_id, response_id):
    try:
        user_id = get_current_user_id()
        deleted = delete_response_service(report_id, response_id,user_id)
        if not deleted:
            abort(403, "No autorizado o el reporte no está abierto")
        return serialize_response(deleted), 204
    except ServiceError as se:
        msg = str(se)
        if msg == 'Reporte no encontrado' or msg == 'Respuesta no encontrada':
            return {'message': msg}, 404
        if msg == 'No se pueden eliminar respuestas de un reporte cerrado' or msg == 'Usuarios solo pueden eliminar sus propias respuestas':
            return {'message': msg}, 403
        if msg == 'Usuario no existe':
            return {'message': msg}, 400
        # fallback
        return {'message': msg}, 400

    except Exception as e:
        return {'message': str(e)}, 500
