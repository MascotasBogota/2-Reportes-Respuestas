from flask_restx import Namespace, Resource

ns = Namespace("reports", description="Endpoints de reportes")

@ns.route("/health")
class HealthResource(Resource):
    def get(self):
        return {"status": "ok"}, 200