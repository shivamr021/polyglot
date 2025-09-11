from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models
from app.intents.utils import get_college_by_name, _normalize_for_query

def handle_scholarship_query(params: dict, db: Session) -> str:
    college_name = params.get("college")
    course_name = params.get("course") # Assuming users might ask "scholarships for btech"

    if not college_name:
        return "Please specify a college to find scholarships."

    college = get_college_by_name(db, college_name)
    if not college:
        return f"Sorry, I couldn't find a college named '{college_name}'."

    query = db.query(models.Scholarship).filter(models.Scholarship.college_id == college.id)

    if course_name:
        # Normalize and filter by course eligibility
        normalized_course = course_name.lower().replace('.', '').replace(' ', '')
        query = query.filter(_normalize_for_query(models.Scholarship.course_eligibility).ilike(f"%{normalized_course}%"))

    scholarships = query.all()

    if not scholarships:
        return f"I couldn't find any scholarship information for {college.name} matching your criteria."

    response_parts = [f"Here are the scholarships available at {college.name}:"]
    for sch in scholarships:
        response_parts.append(f"- {sch.name}: Amount ₹{sch.amount:,.2f}, Deadline: {sch.deadline.strftime('%B %d, %Y')}. Eligibility: {sch.course_eligibility}.")

    return " ".join(response_parts)

