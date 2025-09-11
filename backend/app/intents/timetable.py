from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models
from app.intents.utils import get_college_by_name, _normalize_for_query

def handle_timetable_query(params: dict, db: Session) -> str:
    college_name = params.get("college")
    course_name = params.get("course")
    semester = params.get("semester")

    if not college_name:
        return "Please specify a college to get the timetable."

    college = get_college_by_name(db, college_name)
    if not college:
        return f"Sorry, I couldn't find a college named '{college_name}'."

    query = db.query(models.Timetable).filter(models.Timetable.college_id == college.id)

    if course_name:
        # Normalize and filter by course
        normalized_course = course_name.lower().replace('.', '').replace(' ', '')
        query = query.filter(_normalize_for_query(models.Timetable.course).ilike(f"%{normalized_course}%"))

    if semester:
        query = query.filter(models.Timetable.semester == int(semester))

    timetables = query.all()

    if not timetables:
        return f"I couldn't find any timetable information for {college.name} matching your criteria."

    response_parts = [f"Here are the timetables for {college.name}:"]
    for tt in timetables:
        # FIX: Use the correct attribute 'course' in the response string.
        response_parts.append(f"- For {tt.course} Semester {tt.semester}, you can find the timetable here: {tt.timetable_url}")

    return " ".join(response_parts)

