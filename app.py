"""
ShopMate AI - Flask Application Factory and Configuration

This module sets up the core Flask application with:
- Database configuration (PostgreSQL/SQLite)
- Session management and security
- SQLAlchemy ORM initialization
- Proxy fix for deployment environments
- Debug logging configuration
"""

import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure debug logging for development
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    Provides common functionality and configuration for database models.
    """
    pass

# Initialize SQLAlchemy with the custom base class
db = SQLAlchemy(model_class=Base)

# Create the Flask application instance
app = Flask(__name__)

# Configure application security and sessions
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Add proxy fix for deployment environments (handles HTTPS redirects properly)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Database configuration - supports both PostgreSQL (production) and SQLite (development)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///shopmate.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,    # Recycle connections every 5 minutes
    "pool_pre_ping": True,  # Verify connections before use
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disable event system for performance

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Create database tables within application context
with app.app_context():
    # Import models to register them with SQLAlchemy
    import models
    # Create all tables defined in models
    db.create_all()

# Import and register all routes
import routes
