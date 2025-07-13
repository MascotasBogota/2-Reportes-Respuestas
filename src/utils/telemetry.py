from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
from flask import request
import time

# Definir métricas globales de Prometheus
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0]  # Definir buckets para la latencia en segundos
)

ERROR_COUNT = Counter(
    'http_errors_total',
    'Total number of HTTP errors',
    ['method', 'endpoint', 'status_code']
)

def init_telemetry(app):
    """
    Inicializa la telemetría para la aplicación Flask.
    Configura contadores de peticiones, latencia y errores.
    """
    # Instrumentar Flask automáticamente
    FlaskInstrumentor().instrument_app(app)

    @app.before_request
    def before_request():
        """
        Se ejecuta antes de cada petición.
        Marca el tiempo de inicio y cuenta la petición.
        """
        request._start_time = time.time()
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=str(request.endpoint or 'none')
        ).inc()

    @app.after_request
    def after_request(response):
        """
        Se ejecuta después de cada petición.
        Calcula la latencia y registra errores si los hay.
        """
        # Calcular y registrar la latencia
        latency = time.time() - request._start_time
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=str(request.endpoint or 'none')
        ).observe(latency)

        # Registrar errores (código >= 400)
        if response.status_code >= 400:
            ERROR_COUNT.labels(
                method=request.method,
                endpoint=str(request.endpoint or 'none'),
                status_code=str(response.status_code)
            ).inc()

        return response

    @app.route("/metrics")
    def metrics():
        """
        Endpoint que expone las métricas en formato Prometheus.
        """
        return generate_latest(REGISTRY), 200, {'Content-Type': 'text/plain; version=0.0.4'}