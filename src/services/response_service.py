from src.models.response_model import Response
from src.models.report_model import Report
#from src.utils.auth import verify_user_exists
from mongoengine import DoesNotExist
import datetime as dt


class ServiceError(Exception): pass

def create_response_service(report_id: str, data: dict, user_id: str) -> dict:
    # 1) Verificar que el reporte existe y está abierto
    try:
        report = Report.objects.get(id=report_id)
    except DoesNotExist:
        raise ServiceError('Reporte no encontrado')
    if report.status != 'open':
        raise ServiceError('No se pueden agregar respuestas a un reporte cerrado')
    
    # Forzar imagen para hallazgos

    if data['type'] == 'hallazgo' and not data.get('images'):
        raise ServiceError('Los hallazgos deben incluir al menos una imagen')

    # 2) Verificar que user_id existe (modo producción)
    #if not verify_user_exists(user_id):
      #  raise ServiceError('Usuario no existe')

    # 3) Crear y guardar la respuesta
    resp = Response(
        report_id=report_id,
        resp_user_id=user_id,
        type=data['type'],
        comment=data['comment'],
        images=data.get('images', []),  # Lista de URLs de imágenes opcional
        location=data.get('location')
    )
    resp.save()
    return resp

def get_response_service(report_id: str, response_id: str) -> dict:
    # 1) Verificar que el reporte existe 
    try:
        report = Report.objects.get(id=report_id)
    except DoesNotExist:
        raise ServiceError('Reporte no encontrado')

    # 3) Obtener la respuesta por ID
    try:
        response = Response.objects.get(id=response_id, report_id=report_id)
    except DoesNotExist:
        raise ServiceError('Respuesta no encontrada')
    
    return response 

def get_all_responses_service(report_id: str):
    try:
        report = Report.objects.get(id=report_id)
    except DoesNotExist:
        raise ServiceError('Reporte no encontrado')
    try:
        response = Response.objects(report_id=report_id)
    except DoesNotExist:
        raise ServiceError('No hay ninguna respuesta para este reporte')

    return response

def update_response_service(report_id:str,response_id:str,data: dict, user_id: str):
    try: #verificar existencia de la respuesta
        response = Response.objects.get(id=response_id,report_id=report_id)
    except DoesNotExist:
        raise ServiceError('Respuesta no encontrada')

    try: # verificar que el reporte este abierto
        report:Report = Report.objects.get(id=report_id)
        if report.status != 'open':
            raise ServiceError("No se pueden cambiar respuestas de un reporte cerrado")
    except DoesNotExist:
        raise ServiceError("Reporte no encontrado")
    
    # verificar que el usuario sea el mismo en ambos casos
    if response.resp_user_id != report.user_id:
        raise ServiceError('Usuarios solo pueden modificar sus propias respuestas')
    
    #hacer los cambios
    response.type = data.get('type', response.type)
    response.comment = data.get('comment', response.comment)
    response.location = data.get('location', response.location)
    response.images = data.get('images', response.images)
    response.updated_at = dt.datetime.utcnow()
    response.save()
    return response

def delete_response_service(report_id:str,response_id:str,user_id: str):
    try: #verificar existencia de la respuesta
        response = Response.objects.get(id=response_id,report_id=report_id)
    except DoesNotExist:
        raise ServiceError('Respuesta no encontrada')
    
    try: # verificar que el reporte este abierto
        report:Report = Report.objects.get(id=report_id)
        if report.status != 'open':
            raise ServiceError("No se pueden eliminar respuestas de un reporte cerrado")
    except DoesNotExist:
        raise ServiceError("Reporte no encontrado")
    
    if response.resp_user_id != report.user_id:
        raise ServiceError('Usuarios solo pueden eliminar sus propias respuestas')
    
    response.delete()
    return response