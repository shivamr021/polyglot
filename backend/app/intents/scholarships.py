from sqlalchemy.orm import Session
from app import models

def handle_scholarship_query(params: dict, db: Session) -> str:
    college_name = params.get("college")

    if not college_name:
        return "Please provide a college name to fetch scholarships."

    college = db.query(models.College).filter_by(name=college_name).first()
    if not college:
        return f"College '{college_name}' not found."

    scholarships = db.query(models.Scholarship).filter_by(college_id=college.id).all()

    if not scholarships:
        return f"No scholarships found for {college_name}."

    response = f"Scholarships at {college_name}: "
    for s in scholarships:
        response += f"\n- {s.name}: {s.amount} (Deadline: {s.deadline})"
    return response
