from sqlalchemy.orm import Session
from app import models
from app.intents.utils import get_college_by_name

def handle_scholarship_query(params: dict, db: Session) -> str:
    college_name = params.get("college")

    if not college_name:
        return "Please provide a college name to fetch scholarships."

    college = get_college_by_name(db, college_name)
    if not college:
        return f"Sorry, I couldn’t find a college named '{college_name}'."
    scholarships = db.query(models.Scholarship).filter_by(college_id=college.id).all()

    if not scholarships:
        return f"No scholarships found for {college.name}."

    response = f"Scholarships at {college.name}: "
    for s in scholarships:
        response += f"\n- {s.name}: {s.amount} (Deadline: {s.deadline})"
    return response

