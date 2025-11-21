"""Flask application factory."""
import os
from flask import Flask
from config import config


def create_app(config_name: str = 'default') -> Flask:
    """
    Create and configure the Flask application.
    
    Args:
        config_name: Configuration name to use (default, development, production)
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Register blueprints
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    
    return app

