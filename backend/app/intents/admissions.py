from sqlalchemy.orm import Session
from app import models

def handle_admission_query(params: dict, db: Session) -> str:
    course = params.get("course")
    college_name = params.get("college")

    if not (course and college_name):
        return "Please provide both course and college."

    college = db.query(models.College).filter_by(name=college_name).first()
    if not college:
        return f"College '{college_name}' not found."

    admission = db.query(models.Admission).filter_by(
        college_id=college.id, program=course
    ).first()

    if admission:
        return f"Admission details for {course} at {college_name}: " \
               f"Start Date: {admission.start_date}, " \
               f"Deadline: {admission.deadline}, " \
               f"Criteria: {admission.criteria}"
    return f"No admission details available for {course} at {college_name}."
