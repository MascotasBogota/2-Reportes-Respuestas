from src.models.report_model import Report
from datetime import datetime
from mongoengine.queryset.visitor import Q
from mongoengine import ValidationError
from mongoengine.errors import DoesNotExist

def create_report(data, user_id):
    try:
        return Report(
            user_id=user_id,
            pet_name=data['pet_name'],
            type=data['type'],
            description=data['description'],
            location=data['location'],
            images=data.get('images', [])
        ).save()
    except (ValidationError, KeyError, TypeError) as e:
        raise ValueError("Error de validación en datos del reporte: " + str(e))



def update_report(report_id, data, user_id):
    try:
        report = Report.objects(id=report_id, user_id=user_id, status='open').first()
        if not report:
            return None

        report.pet_name = data.get('pet_name', report.pet_name)
        report.type = data.get('type', report.type)
        report.description = data.get('description', report.description)
        report.location = data.get('location', report.location)
        report.images = data.get('images', report.images)
        report.updated_at = datetime.utcnow()
        report.save()
        return report
    except Exception as e:
        raise ValueError("Error al actualizar el reporte: " + str(e))


def delete_report(report_id, user_id):
    try:
        report = Report.objects(id=report_id, user_id=user_id, status='open').first()
        if not report:
            return False
        report.delete()
        return True
    except Exception as e:
        raise ValueError("Error al eliminar el reporte: " + str(e))


def close_report(report_id, user_id):
    try:
        report = Report.objects(id=report_id, user_id=user_id, status='open').first()
        if not report:
            return None
        report.status = "closed"
        report.closed_at = datetime.utcnow()
        report.save()
        return report
    except Exception as e:
        raise ValueError("Error al cerrar el reporte: " + str(e))



def get_report_by_id(report_id):
    return Report.objects(id=report_id).first()



def get_filtered_reports(report_type=None, location=None, radius=None):
    query = Q()

    if report_type:
        query &= Q(type=report_type)

    if location and radius:
        # MongoDB espera GeoJSON con [long, lat]
        query &= Q(location__geo_within_center=[location, radius / 111000])  # metros a grados

    return Report.objects(query, status="open")


