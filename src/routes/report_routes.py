from flask_restx import Namespace, Resource, fields
from src.controllers import report_controller

ns = Namespace("reportes", description="Gestión de reportes de mascotas")

# Esquema para ubicación (GeoJSON Point)
location_model = ns.model('Location', {
    'type': fields.String(example="Point", required=True),
    'coordinates': fields.List(fields.Float, example=[-74.08, 4.6], required=True)
})

# Esquema de entrada para creación y actualización de reportes
report_input = ns.model('ReportInput', {
    'type': fields.String(required=True, enum=['perro', 'gato', 'otro']),
    'description': fields.String(required=True),
    'location': fields.Nested(location_model, required=True),
    'images': fields.List(fields.String, required=False)  # base64 o URLs
})

@ns.route("/")
class ReportCreate(Resource):
    @ns.expect(report_input)
    @ns.response(201, "Reporte creado exitosamente")
    @ns.response(400, "Faltan campos obligatorios o el formato es incorrecto")
    @ns.response(401, "Token de autenticación inválido")
    @ns.response(500, "Error al crear el reporte")
    def post(self):
        """Crear nuevo reporte"""
        return report_controller.create_report_controller()

@ns.route("/<string:report_id>")
class ReportUpdateDelete(Resource):
    @ns.expect(report_input)
    @ns.response(200, "Reporte actualizado")
    def put(self, report_id):
        """Actualizar reporte propio"""
        return report_controller.update_report_controller(report_id)

    @ns.response(204, "Reporte eliminado")
    def delete(self, report_id):
        """Eliminar reporte propio"""
        return report_controller.delete_report_controller(report_id)


@ns.route("/<string:report_id>/close")
class ReportClose(Resource):
    @ns.response(200, "Reporte cerrado exitosamente")
    def post(self, report_id):
        """Marcar reporte como 'Encontrado'"""
        return report_controller.close_report_controller(report_id)

@ns.route("/pingdb")
class PingDB(Resource):
    def get(self):
        """Verifica conexión a la base de datos"""
        from src.models.report_model import Report
        try:
            # intenta contar documentos (aunque no haya ninguno aún)
            count = Report.objects.count()
            return {"status": "OK", "reports_in_db": count}, 200
        except Exception as e:
            return {"status": "ERROR", "error": str(e)}, 500