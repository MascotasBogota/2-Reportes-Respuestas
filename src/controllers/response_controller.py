from flask import jsonify, request
from src.services.response_service import create_response_service,get_response_service, ServiceError
from src.utils.auth import get_current_user_id
from src.utils.serialization import serialize_response


def add_response_controller(report_id):
    user_id = get_current_user_id()
    if not user_id:
        return {'message': 'Token inválido o no autenticado'}, 401

    data = request.get_json() or {}
    try:
        result = create_response_service(report_id, data, user_id)
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
        print("before serializin")
        print(f"\nresult is {result}\n")	
        return result, 200

    except ServiceError as se:
        print("SERVICE ERROR-----------")
        # Errores controlados (404, 403, 400 según mensaje)
        msg = str(se)
        if msg == 'Reporte no encontrado' or msg == 'Respuesta no encontrada':
            return {'message': msg}, 404
        # fallback
        return {'message': msg}, 400

    except Exception as e:
        print("SERVICE ERROR----------- NOTTTT")
        return {'message': str(e)}, 500