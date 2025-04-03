from marshmallow import fields, Schema, validate
from datetime import datetime

class ResumeSchema(Schema):
    _id = fields.String(dump_only=True)
    user_name=fields.String(required=True)
    user_id = fields.String(required=True)  # Reference to User collection
    file_url = fields.String(required=True)  # Cloud storage URL
    job_id=fields.String(required=True)
    # Ensure skills are non-empty and have a reasonable length
    skills = fields.List(fields.String(validate=validate.Length(min=1, max=50)), required=True)

    # Ensure experience is a non-negative integer
    experience = fields.Integer(required=True, validate=validate.Range(min=0))
    resume_text=fields.String()

    # Auto-set created_at timestamp
    created_at = fields.DateTime(dump_only=True, missing=lambda: datetime.now())