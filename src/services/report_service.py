from src.models.report_model import Report
from datetime import datetime
from mongoengine.queryset.visitor import Q

def create_report(data, user_id):
    report = Report(
        user_id=user_id,
        type=data['type'],
        description=data['description'],
        location=data['location'],
        images=data.get('images', []),
    )
    report.save()
    return report

def update_report(report_id, data, user_id):
    report = Report.objects(id=report_id, user_id=user_id, status='open').first()
    if not report:
        return None
    report.type = data.get('type', report.type)
    report.description = data.get('description', report.description)
    report.location = data.get('location', report.location)
    report.images = data.get('images', report.images)
    report.updated_at = datetime.utcnow()
    report.save()
    return report

def delete_report(report_id, user_id):
    report = Report.objects(id=report_id, user_id=user_id, status='open').first()
    if not report:
        return False
    report.delete()
    return True

def close_report(report_id, user_id):
    report = Report.objects(id=report_id, user_id=user_id, status='open').first()
    if not report:
        return None
    report.status = "closed"
    report.closed_at = datetime.utcnow()
    report.save()
    return report


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


