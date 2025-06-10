from src.models.report_model import Report
from datetime import datetime

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
