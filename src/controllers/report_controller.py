from flask import request
from flask_restx import abort
from src.services import report_service
from src.utils.auth import get_current_user_id

def create_report_controller():
    data = request.json
    user_id = "user_dev_123"  # valor simulado
    report = report_service.create_report(data, user_id)
    return report.to_mongo().to_dict(), 201

def update_report_controller(report_id):
    user_id = get_current_user_id()
    data = request.json
    report = report_service.update_report(report_id, data, user_id)
    if not report:
        abort(403, "No autorizado o el reporte no está abierto")
    return report.to_mongo().to_dict(), 200

def delete_report_controller(report_id):
    user_id = get_current_user_id()
    deleted = report_service.delete_report(report_id, user_id)
    if not deleted:
        abort(403, "No autorizado o el reporte no está abierto")
    return '', 204

def close_report_controller(report_id):
    user_id = get_current_user_id()
    report = report_service.close_report(report_id, user_id)
    if not report:
        abort(403, "No autorizado o el reporte ya está cerrado")
    return report.to_mongo().to_dict(), 200
