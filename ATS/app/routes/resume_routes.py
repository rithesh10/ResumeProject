from flask import Blueprint
from app.controllers.resume_controller import upload_resume, get_by_jobId,get_by_Id
from app.middleware.auth_middleware import verify_jwt

# Create a Blueprint for resumes
resume_bp = Blueprint("resume", __name__)

# Register the routes with middleware
@resume_bp.route("/upload-resume", methods=["POST"])
@verify_jwt
def upload():
    return upload_resume()

@resume_bp.route("/get-resume-jobId/<id>", methods=["GET"])
@verify_jwt
def get_resumes(id):
    return get_by_jobId(id)
@resume_bp.route("/<id>",methods=["GET"])
def get_resumeId(id):
    return get_by_Id(id)
