from flask import request
from flask_restx import abort
from src.services import report_service
from src.utils.auth import get_current_user_id
from src.utils.serialization import serialize_report

def create_report_controller():
    try:
        data = request.get_json(force=True) or {}

        required_fields = ['type', 'description', 'location']
        for field in required_fields:
            if field not in data or not data[field]:
                abort(400, f"Falta el campo obligatorio: {field}")

        user_id = get_current_user_id()
        report = report_service.create_report(data, user_id)
        return serialize_report(report), 201

    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        print(f"[ERROR] {e}")
        abort(500, "Error al crear el reporte")


def update_report_controller(report_id):
    try:
        user_id = get_current_user_id()
        data = request.json or {}

        if not isinstance(data, dict):
            abort(400, "El cuerpo de la solicitud debe ser JSON")

        report = report_service.update_report(report_id, data, user_id)
        if not report:
            abort(403, "No autorizado o el reporte no está abierto")
        return serialize_report(report), 200

    except ValueError as ve:
        abort(400, str(ve))
    except Exception as e:
        print(f"Error al actualizar reporte: {e}")
        abort(500, "Error al actualizar el reporte")


def delete_report_controller(report_id):
    try:
        user_id = get_current_user_id()
        deleted = report_service.delete_report(report_id, user_id)
        if not deleted:
            abort(403, "No autorizado o el reporte no está abierto")
        return '', 204

    except Exception as e:
        print(f"Error al eliminar reporte: {e}")
        abort(500, "Error al eliminar el reporte")


def close_report_controller(report_id):
    try:
        user_id = get_current_user_id()
        report = report_service.close_report(report_id, user_id)
        if not report:
            abort(403, "No autorizado o el reporte ya está cerrado")
        return serialize_report(report), 200

    except Exception as e:
        print(f"Error al cerrar reporte: {e}")
        abort(500, "Error al cerrar el reporte")


def get_filtered_reports_controller():
    from src.services import report_service
    from src.utils.serialization import serialize_report

    report_type = request.args.get("type")
    try:
        lng = float(request.args.get("lng")) if request.args.get("lng") else None
        lat = float(request.args.get("lat")) if request.args.get("lat") else None
        radius = float(request.args.get("radius")) if request.args.get("radius") else None
    except ValueError:
        abort(400, "Parámetros de ubicación inválidos")

    location = [lng, lat] if lng is not None and lat is not None else None
    reports = report_service.get_filtered_reports(report_type, location, radius)
    return [serialize_report(r) for r in reports], 200

def get_report_by_id_controller(report_id):
    try:
        report = report_service.get_report_by_id(report_id)
        if not report:
            abort(404, "Reporte no encontrado")
        return serialize_report(report), 200
    except (ValidationError, DoesNotExist):
        abort(400, "ID inválido")
