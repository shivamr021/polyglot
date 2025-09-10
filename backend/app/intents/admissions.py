from sqlalchemy.orm import Session
from app import models
from app.intents.utils import get_college_by_name

def handle_admission_query(params: dict, db: Session) -> str:
    course = params.get("course")
    college_name = params.get("college")

    if not (course and college_name):
        return "Please provide both course and college."

    college = get_college_by_name(db, college_name)
    if not college:
        return f"Sorry, I couldn’t find a college named '{college_name}'."
    admission = db.query(models.Admission).filter_by(
        college_id=college.id, program=course
    ).first()

    if admission:
        return f"Admission details for {course} at {college.name}: " \
               f"Start Date: {admission.start_date}, " \
               f"Deadline: {admission.deadline}, " \
               f"Criteria: {admission.criteria}"
    return f"No admission details available for {course} at {college.name}."

