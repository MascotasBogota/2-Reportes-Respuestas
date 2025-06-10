from datetime import datetime
from bson import ObjectId

def serialize_report(report):
    if hasattr(report, "to_mongo"):
        doc = report.to_mongo().to_dict()
    else:
        doc = dict(report)  # por si acaso

    doc["_id"] = str(report.id)  # ObjectId a str

    for key, value in doc.items():
        if isinstance(value, datetime):
            doc[key] = value.isoformat()
        elif isinstance(value, ObjectId):
            doc[key] = str(value)

    return doc
