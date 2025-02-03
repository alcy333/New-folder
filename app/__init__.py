from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from datetime import datetime

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
socketio = SocketIO()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    socketio.init_app(app)
    
    login_manager.login_view = 'auth.login'

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.products import products_bp
    from app.routes.bids import bids_bp
    from app.routes.ws import ws_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(bids_bp)
    app.register_blueprint(ws_bp)

    # User loader
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    @app.template_filter('time_remaining')
    def time_remaining_filter(end_time):
        now = datetime.utcnow()
        delta = end_time - now
        if delta.total_seconds() < 0:
            return "Expired"
        hours, remainder = divmod(delta.seconds, 3600)
        minutes = remainder // 60
        return f"{hours}h {minutes}m"

    return app