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

def serialize_response(response):
    print("serializin")
    if hasattr(response, "to_mongo"):
        doc = response.to_mongo().to_dict()
    else:
        doc = dict(response)
    
    print(doc)

    # Reemplazar _id por id
    doc["id"] = str(doc.pop("_id"))

    def convert(value):
        if isinstance(value, ObjectId):
            return str(value)
        elif isinstance(value, datetime):
            return value.isoformat()
        elif isinstance(value, list):
            return [convert(item) for item in value]
        elif isinstance(value, dict):
            return {k: convert(v) for k, v in value.items()}
        else:
            return value

    return {k: convert(v) for k, v in doc.items()}