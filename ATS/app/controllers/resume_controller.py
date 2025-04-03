import os
from marshmallow import ValidationError
from flask import request, jsonify,g
from werkzeug.utils import secure_filename
from app.services.cloudinary_service import upload_to_cloudinary  # Your Cloudinary upload function
import fitz
from docx import Document 
from app.models.Resume_Model import ResumeSchema
from datetime import datetime,timezone
from db.db import mongo
from bson import ObjectId,json_util
resume_schema=ResumeSchema()

UPLOAD_FOLDER = "public/temp"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf", "docx"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text(file, filename):
    """
    Extracts text from PDF, DOC, and DOCX files.
    """
    try:
        file_ext = filename.split(".")[-1].lower()

        if file_ext == "pdf":
            file.seek(0)  # Reset pointer before reading
            pdf_document = fitz.open(stream=file.read(), filetype="pdf")
            text = "\n".join([page.get_text("text") for page in pdf_document])

        elif file_ext == "docx":
            file.seek(0)  # Reset pointer before reading
            doc = Document(file)
            text = "\n".join([para.text for para in doc.paragraphs])

        else:
            return None  # Unsupported file type

        return text.strip()

    except Exception as e:
        print("Error extracting text:", str(e))
        return None

def upload_resume():
    try:
        # ✅ 1. Check if the file exists
        
        # ✅ Make sure request.user exists before accessing "_id"
        # print(g.user._id)

        if "resume" not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files["resume"]

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        filename = secure_filename(file.filename)

        # ✅ 2. Validate file type
        if not allowed_file(filename):
            return jsonify({"error": "Invalid file type. Only PDF and DOCX allowed"}), 400

        # ✅ 3. Extract text before uploading
        file.seek(0)  # Reset file pointer
        extracted_text = extract_text(file, filename)

        # ✅ 4. Upload file to Cloudinary or Storage
        file.seek(0)  # Reset again before uploading
        resume_url = upload_to_cloudinary(file)
        
        # ✅ 5. Extract other form data (NOT JSON)
        user_name=g.user["full_name"]
        user_id = g.user["_id"]  # Extract from JWT
        skills = request.form.getlist("skills")  # Extract list
        experience = request.form.get("experience", 0)
        job_id=request.form.get("_id")
        # job_idjob_id)
        # Convert experience to integer safely
        try:
            experience = int(experience)
        except ValueError:
            return jsonify({"error": "Experience must be a valid integer"}), 400

        # ✅ 6. Create the resume document
        resume = {
            "user_id": user_id,
            "file_url": resume_url,
            "user_name":user_name,
            "skills": skills,
            "job_id":job_id,
            "experience": experience,
            "resume_text":extracted_text
            # "created_at": datetime.now(timezone.utc)
        }
        # print(resume)

        # ✅ 7. Validate schema
        errors = resume_schema.validate(resume)
        if errors:
            return jsonify({"error": "Validation failed", "details": errors}), 400
        
        # ✅ 8. Insert into MongoDB
        resume= mongo.db.resume.insert_one(resume)
        # print(resume)

        # ✅ 9. Return success response
        return jsonify({
            "message": "Resume uploaded successfully",
            # "resume": resume
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
from flask import jsonify
from bson import json_util, ObjectId

def get_by_jobId(id):
    resumes = mongo.db.resume.find({"job_id": id})  # Fetch resumes matching job_id
    resumes_list = list(resumes)  # Convert cursor to list

    if not resumes_list:
        return jsonify({"message": "No resumes found"}), 404

    # Convert `_id` from ObjectId to string for all resumes
    for resume in resumes_list:
        resume["_id"] = str(resume["_id"])

    return jsonify({
        "message": "Fetched successfully",
        "resumes": resumes_list  # Directly return list (no need for json_util.dumps)
    }), 200

from flask import jsonify
from bson import ObjectId, json_util

def get_by_Id(id):
    try:
        object_id = ObjectId(id)  # ✅ Convert id to ObjectId before querying
    except:
        return jsonify({"message": "Invalid ID format"}), 400  # Handle invalid ObjectId

    resume = mongo.db.resume.find_one({"_id": object_id})  # ✅ `find_one()` returns a dictionary
    resume["_id"]=ObjectId(resume["_id"])
    if not resume:
        return jsonify({"message": "No resume found"}), 404  # ✅ Fixed message

    return jsonify({
        "message": "Fetched successfully",
        "resume": json_util.loads(json_util.dumps(resume))  # ✅ Convert BSON to JSON
    }), 200
