from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO
from config import config
import redis

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
ma = Marshmallow()
socketio = SocketIO()
redis_client = None

def create_app(config_name):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    CORS(app, origins=app.config['CORS_ORIGINS'])

    # Initialize Redis
    global redis_client
    redis_client = redis.from_url(app.config['REDIS_URL'])

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.buses import buses_bp
    from app.routes.drivers import drivers_bp
    from app.routes.routes import routes_bp
    from app.routes.students import students_bp
    from app.routes.trips import trips_bp
    from app.routes.maintenance import maintenance_bp
    from app.routes.attendance import attendance_bp
    from app.routes.fees import fees_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.tracking import tracking_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(buses_bp, url_prefix='/api/buses')
    app.register_blueprint(drivers_bp, url_prefix='/api/drivers')
    app.register_blueprint(routes_bp, url_prefix='/api/routes')
    app.register_blueprint(students_bp, url_prefix='/api/students')
    app.register_blueprint(trips_bp, url_prefix='/api/trips')
    app.register_blueprint(maintenance_bp, url_prefix='/api/maintenance')
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
    app.register_blueprint(fees_bp, url_prefix='/api/fees')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(tracking_bp, url_prefix='/api/tracking')

    # Error handlers
    @app.errorhandler(404)
    def not_found(_):
        return {'error': 'Resource not found'}, 404

    @app.errorhandler(500)
    def internal_error(_):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(_, __):
        return {'error': 'Token has expired'}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(_):
        return {'error': 'Invalid token'}, 401

    @jwt.unauthorized_loader
    def missing_token_callback(_):
        return {'error': 'Authorization token is required'}, 401

    return app
