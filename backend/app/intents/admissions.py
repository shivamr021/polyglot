from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models
from app.intents.utils import get_college_by_name, _normalize_for_query

def handle_admission_query(params: dict, db: Session) -> str:
    college_name = params.get("college")
    course_name = params.get("course")

    if not college_name:
        return "Please specify a college name to check admission details."

    college = get_college_by_name(db, college_name)
    if not college:
        return f"Sorry, I couldn’t find a college named '{college_name}'."

    query = db.query(models.Admission).filter(models.Admission.college_id == college.id)

    if course_name:
        # Normalize and filter by course if provided
        normalized_course = course_name.lower().replace('.', '').replace(' ', '')
        query = query.filter(_normalize_for_query(models.Admission.course).ilike(f"%{normalized_course}%"))

    admissions = query.all()

    if not admissions:
        response = f"No admission information found for {college.name}"
        if course_name:
            response += f" for the {course_name} course."
        return response

    response_parts = [f"Admission details for {college.name}:"]
    for adm in admissions:
        # FIX: Use the correct attribute 'course' in the response string.
        response_parts.append(f"- For {adm.course}, the process is: {adm.process}. The last date to apply is {adm.last_date.strftime('%B %d, %Y')}.")
    
    return " ".join(response_parts)

