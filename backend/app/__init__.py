from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.errors import RateLimitExceeded
from flask_limiter.util import get_remote_address

from app.blueprints import catalogos_bp, health_bp, servidores_bp
from app.blueprints.stats import stats_bp
from app.logging_setup import configure_logging
from app.config import Config
from app.db import close_connection
from app.errors import ApiError, TooManySearchesError


def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=[app.config["RATE_LIMIT"]],
        storage_uri="memory://",
    )
    limiter.limit(app.config["RATE_LIMIT"])(servidores_bp)

    configure_logging()
    app.register_blueprint(health_bp)
    app.register_blueprint(servidores_bp)
    app.register_blueprint(catalogos_bp)
    app.register_blueprint(stats_bp)
    app.teardown_appcontext(close_connection)

    @app.errorhandler(ApiError)
    def handle_api_error(error: ApiError):
        return jsonify(error.to_dict()), error.status_code

    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit(_error):
        excess = TooManySearchesError(
            "Limite de consultas por minuto excedido. Aguarde e tente novamente."
        )
        return jsonify(excess.to_dict()), excess.status_code

    @app.errorhandler(404)
    def handle_not_found(_error):
        return jsonify(
            {"error": "pagina_inexistente", "message": "Recurso ou rota não encontrada."}
        ), 404

    @app.errorhandler(405)
    def handle_method(_error):
        return jsonify(
            {"error": "parametro_invalido", "message": "Método HTTP não permitido nesta rota."}
        ), 405

    @app.errorhandler(500)
    def handle_internal(_error):
        return jsonify(
            {"error": "erro_interno", "message": "Falha inesperada ao processar a consulta."}
        ), 500

    return app
