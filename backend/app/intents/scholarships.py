from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models
from app.intents.utils import get_college_by_name, _normalize_for_query

def handle_scholarship_query(params: dict, db: Session) -> str:
    college_name = params.get("college")
    course_param = params.get("course") # Assuming users might ask "scholarships for btech"

    if not college_name:
        return "Please specify a college to find scholarships."

    college = get_college_by_name(db, college_name)
    if not college:
        return f"Sorry, I couldn't find a college named '{college_name}'."

    query = db.query(models.Scholarship).filter(models.Scholarship.college_id == college.id)

    # FIX 1: Handle when 'course' is a list from Dialogflow
    if course_param:
        # If it's a list, take the first element; otherwise, use it as is.
        course_name = course_param[0] if isinstance(course_param, list) else course_param
        
        # Normalize and filter by course eligibility
        normalized_course = course_name.lower().replace('.', '').replace(' ', '')
        # FIX 2: Use the correct column name 'eligibility'
        query = query.filter(_normalize_for_query(models.Scholarship.eligibility).ilike(f"%{normalized_course}%"))

    scholarships = query.all()

    if not scholarships:
        return f"I couldn't find any scholarship information for {college.name} matching your criteria."

    response_parts = [f"Here are the scholarships available at {college.name}:"]
    for sch in scholarships:
        # FIX 2: Use the correct attribute 'eligibility' in the response
        response_parts.append(f"- {sch.name}: Amount ₹{sch.amount:,.2f}, Deadline: {sch.deadline.strftime('%B %d, %Y')}. Eligibility: {sch.eligibility}.")

    return " ".join(response_parts)

