from src.models.response_model import Response
from src.models.report_model import Report
#from src.utils.auth import verify_user_exists
from mongoengine import DoesNotExist

class ServiceError(Exception): pass

def create_response_service(report_id: str, data: dict, user_id: str) -> dict:
    # 1) Verificar que el reporte existe y está abierto
    try:
        report = Report.objects.get(id=report_id)
    except DoesNotExist:
        raise ServiceError('Reporte no encontrado')
    if report.status != 'open':
        raise ServiceError('No se pueden agregar respuestas a un reporte cerrado')

    # 2) Verificar que user_id existe (modo producción)
    #if not verify_user_exists(user_id):
      #  raise ServiceError('Usuario no existe')

    # 3) Crear y guardar la respuesta
    resp = Response(
        report_id=report_id,
        resp_user_id=user_id,
        type=data['type'],
        comment=data['comment'],
        location=data.get('location')
    )
    resp.save()
    return resp.to_mongo().to_dict()