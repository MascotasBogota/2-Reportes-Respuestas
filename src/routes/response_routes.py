from flask_restx import fields, Namespace, Resource
from src.controllers.response_controller import add_response_controller
from src.extensions import api

ns = Namespace('responses', description='Respuestas a reportes')

# Define el payload esperado para crear una respuesta
response_model = api.model('ResponseCreate', {
    'type': fields.String(required=True, description='"avistamiento" o "hallazgo"', example='avistamiento'),
    'comment': fields.String(required=True, description='Descripción del avistamiento', example='Lo vi cerca del parque'),
    'location': fields.Nested(api.model('Point', {
        'type': fields.String(required=True, example='Point'),
        'coordinates': fields.List(fields.Float, required=True, example=[-74.03, 4.67])
    }))
})

@ns.route('/<string:report_id>')
@ns.param('report_id', 'ID del reporte al que se responde')
class ResponseListResource(Resource):
    @ns.expect(response_model)
    @ns.response(201, 'Respuesta creada exitosamente')
    @ns.response(400, 'Solicitud inválida')
    @ns.response(401, 'No autenticado')
    @ns.response(403, 'Operación no permitida')
    @ns.response(404, 'Reporte no encontrado')
    def post(self, report_id):
        return add_response_controller(report_id)