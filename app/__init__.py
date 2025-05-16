# app/__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

# module‐level extensions
db      = SQLAlchemy()
migrate = Migrate()

def create_app():
   
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY','1gh3jkt46kmb6v' )
    
    db.init_app(app)
    migrate.init_app(app, db)

    

    # Register blueprints
    from .controllers.home_controller import home_bp
    app.register_blueprint(home_bp)

    from .controllers.preferences_controller import pref_bp
    app.register_blueprint(pref_bp)
    
    from .controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    from .controllers.destination_controller import dest_bp
    app.register_blueprint(dest_bp)

    return app
