from flask import Flask
from config import Config
from db.db import init_mongo, mongo  # Import both
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load config settings

    # Allow CORS for a specific frontend URL (Replace with your actual frontend URL)
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)


    init_mongo(app)  # Initialize MongoDB with app

    # Register Blueprints (modular routes)
    from app.routes.user_routes import user_bp
    from app.routes.resume_routes import resume_bp
    from app.routes.job_routes import job_bp
    from app.routes.resume_rank_routes import resume_ranking_bp

    app.register_blueprint(resume_ranking_bp, url_prefix="/ranking")
    app.register_blueprint(job_bp, url_prefix="/jobs")
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(resume_bp, url_prefix="/resume")

    return app
